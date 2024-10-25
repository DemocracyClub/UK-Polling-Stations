import datetime
from functools import cached_property
from typing import List, Optional
from urllib.parse import urlencode, urljoin

import requests
from dateutil.parser import parse
from django.conf import settings
from django.core.cache import cache
from uk_geo_utils.helpers import Postcode

session = requests.session()


class EveryElectionWrapper:
    def __init__(
        self, postcode=None, point=None, council_id=None, include_current=False
    ):
        self.base_params = {"identifier_type": "ballot", "current": 1}
        if not include_current:
            # When future=1, current-but-past elections are excluded.
            # Only pass future if include_current is False
            self.base_params["future"] = 1
        if not any((postcode, point, council_id)):
            raise ValueError("Expected either a point, postcode or council_id")
        try:
            self.request_success = False
            if postcode:
                self.elections = self.get_data_by_postcode(
                    Postcode(postcode).with_space
                )
                self.request_success = True
            if point:
                self.elections = self.get_data_by_point(point)
                self.request_success = True
            if council_id:
                self.elections = self.get_election_intersecting_local_authority(
                    council_id
                )
                self.request_success = True
            self.ballots = self.get_ballots_for_next_date()
            self.cancelled_ballots = self.get_cancelled_ballots()
        except requests.exceptions.RequestException:
            self.request_success = False

    def get_data_by_postcode(self, postcode):
        params = self.base_params.copy()
        params.update(
            {
                "postcode": postcode,
            }
        )
        root_url = urljoin(settings.EE_BASE, "api/elections.json")
        query_url = f"{root_url}?{urlencode(params)}"

        return self.get_data(query_url)

    def get_data_by_point(self, point):
        params = self.base_params.copy()
        params.update(
            {
                "coords": f"{point.y},{point.x}",
            }
        )

        root_url = urljoin(settings.EE_BASE, "api/elections.json")
        query_url = f"{root_url}?{urlencode(params)}"
        return self.get_data(query_url)

    def get_election_intersecting_local_authority(self, council_id):
        query_url = (
            "%sapi/elections.json?election_intersects_local_authority=%s&future=1&identifier_type=ballot"
            % (
                settings.EE_BASE,
                council_id,
            )
        )
        # Only used by council users in the uploader
        # This query is expensive, so we want to avoid making it too often
        return self.get_data(query_url, cache_hours=0.5)

    def get_data(self, query_url, cache_hours=0):
        res_json = None
        if cache_hours:
            res_json = cache.get(query_url)
        if not res_json:
            headers = {}
            if hasattr(settings, "CUSTOM_UA"):
                headers["User-Agent"] = settings.CUSTOM_UA

            res = session.get(query_url, timeout=10, headers=headers)

            if res.status_code != 200:
                res.raise_for_status()

            res_json = res.json()
            if cache_hours:
                cache.set(query_url, res_json, 60 * 60 * cache_hours)

        if "results" in res_json:
            return res_json["results"]
        return res_json

    def get_all_ballots(self):
        if not self.request_success:
            return []
        ballots = [e for e in self.elections if e["group_type"] is None]
        ballots = [
            e for e in ballots if e["election_id"] not in settings.ELECTION_BLACKLIST
        ]
        return sorted(ballots, key=lambda k: k["poll_open_date"])

    def get_future_election_dates(self):
        if not self.request_success:
            return []
        dates = {e["poll_open_date"] for e in self.elections if not e["cancelled"]}
        return sorted(dates)

    def _get_next_election_date(self):
        ballots = self.get_all_ballots()
        # if no ballots, return early
        if len(ballots) == 0:
            return None
        next_charismatic_election_dates = getattr(
            settings, "NEXT_CHARISMATIC_ELECTION_DATES", []
        )
        next_charismatic_election_dates.sort()
        dates = [b["poll_open_date"] for b in ballots]
        dates.sort()

        if next_charismatic_election_dates:
            # If we have some dates return the first one that is in NEXT_CHARISMATIC_ELECTION_DATES
            for date in dates:
                if date in next_charismatic_election_dates:
                    return date
            # If none of them are in NEXT_CHARISMATIC_ELECTION_DATES,
            # return the earliest charismatic election date
            return next_charismatic_election_dates[0]

        # If we haven't set NEXT_CHARISMATIC_ELECTION_DATES,
        # return the earliest election
        return dates[0]

    def get_ballots_for_next_date(self):
        if not self.request_success:
            return []
        ballots = self.get_all_ballots()
        if len(ballots) == 0:
            return ballots
        next_election_date = self._get_next_election_date()
        return [e for e in ballots if e["poll_open_date"] == next_election_date]

    def get_cancelled_ballots(self):
        return [b for b in self.ballots if b["cancelled"]]

    @property
    def all_ballots_cancelled(self):
        return len(self.cancelled_ballots) > 0 and len(self.ballots) == len(
            self.cancelled_ballots
        )

    def get_cancelled_election_info(self):
        rec = {
            "cancelled": None,
            "name": None,
            "rescheduled_date": None,
            "metadata": None,
        }

        # bypass the rest of this if we're not checking EE
        # or we failed to contact EE
        if not settings.EVERY_ELECTION["CHECK"] or not self.request_success:
            rec["cancelled"] = False
            return rec

        rec["cancelled"] = self.all_ballots_cancelled
        # What we care about here is if _all_
        # applicable ballot objects are cancelled.

        # i.e: If the user has a local election and a mayoral election
        # and the local one is cancelled but the mayoral one is going ahead
        # we just want to tell them where the polling station is.

        # For the purposes of WhereDIV we can abstract
        # the complexity that they will receive a different
        # number of ballots than expected when they get there.
        if not rec["cancelled"]:
            return rec

        cancelled_ballot = self.cancelled_ballots[0]
        if len(self.cancelled_ballots) == 1:
            rec["name"] = cancelled_ballot["election_title"]
        rec["metadata"] = cancelled_ballot["metadata"]

        if cancelled_ballot["replaced_by"]:
            try:
                query_url = "%sapi/elections/%s.json" % (
                    settings.EE_BASE,
                    cancelled_ballot["replaced_by"],
                )
                new_ballot = self.get_data(query_url)
                rec["rescheduled_date"] = datetime.datetime.strptime(
                    new_ballot["poll_open_date"], "%Y-%m-%d"
                ).strftime("%-d %B %Y")
            except requests.exceptions.RequestException:
                rec["rescheduled_date"] = None

        return rec

    def has_election(self, future_only=True):
        if not settings.EVERY_ELECTION["CHECK"]:
            return settings.EVERY_ELECTION["HAS_ELECTION"]

        if not self.request_success:
            # if the request was unsuccessful for some reason,
            # assume there *is* an upcoming election
            return True

        ballots_to_check = self.ballots[:]
        if future_only:
            ballots_to_check = []
            for ballot in self.ballots:
                if parse(ballot["poll_open_date"]).date() >= datetime.date.today():
                    ballots_to_check.append(ballot)

        if len(ballots_to_check) > 0 and not self.all_ballots_cancelled:
            return True
        return False

    def get_explanations(self):
        explanations = []
        if not self.request_success:
            # if the request was unsuccessful for some reason,
            # return no explanations
            return explanations

        if len(self.elections) > 0:
            for election in self.elections:
                if (
                    "explanation" in election
                    and election["explanation"]
                    and election["poll_open_date"] == self._get_next_election_date()
                ):
                    explanations.append(
                        {
                            "title": election["election_title"],
                            "explanation": election["explanation"],
                        }
                    )
        return explanations

    def get_metadata(self):
        cancelled = self.get_cancelled_election_info()
        if cancelled["cancelled"]:
            return {"cancelled_election": cancelled["metadata"]}

        return None

    def get_metadata_by_key(self, key):
        if not settings.EVERY_ELECTION["CHECK"] or not self.request_success:
            return None

        for b in self.ballots:
            if "metadata" in b and b["metadata"] and key in b["metadata"]:
                return b["metadata"][key]
        return None

    def get_voter_id_status(self) -> Optional[str]:
        """
        For a given election, determine whether any ballots require photo ID
        If yes, return the stub value (e.g. EA-2022)
        If no, return None
        """
        ballot_with_id = next(
            (
                ballot
                for ballot in self.get_all_ballots()
                if ballot.get("requires_voter_id") and not ballot.get("cancelled")
            ),
            {},
        )
        return ballot_with_id.get("requires_voter_id")

    @property
    def multiple_elections(self):
        if self.has_election and self.request_success:
            uncancelled_ballots = [b for b in self.ballots if not b["cancelled"]]
            return len(uncancelled_ballots) > 1
        return False


class EmptyEveryElectionWrapper:
    """
    There are times when we know that we don't want to query EE, for example
    when we are going to show an address picker.

    This class allows us to swap out the EveryElectionWrapper while keeping
    exisitng code the same.
    """

    @staticmethod
    def has_election() -> bool:
        return False

    @staticmethod
    def get_metadata() -> None:
        return None

    @staticmethod
    def get_ballots_for_next_date() -> List:
        return []

    @staticmethod
    def get_all_ballots() -> List:
        return []

    @staticmethod
    def multiple_elections():
        return False

    def get_explanations(self):
        return None

    def get_voter_id_status(self):
        return None

    def get_cancelled_election_info(self):
        return {}


class StaticElectionsAPIElectionWrapper:
    def __init__(self, elections_response):
        self.elections_response = elections_response
        self.ballots = []
        for date in self.elections_response["dates"]:
            for ballot in date["ballots"]:
                self.ballots.append(ballot)

    def has_election(self, future_only=True):
        if not self.elections_response["dates"]:
            return False

        if future_only:
            for ballot in self.ballots:
                if parse(ballot["poll_open_date"]).date() >= datetime.date.today():
                    return True
        return False

    @property
    def multiple_elections(self):
        if self.has_election:
            uncancelled_ballots = [b for b in self.ballots if not b["cancelled"]]
            return len(uncancelled_ballots) > 1
        return False

    def get_explanations(self):
        # TODO: This currently isn't in the static JSON so we can't get it without
        #       calling EE. Either call EE (seems silly given where we are) or add
        #       to the JSON (easier and more useful?)
        return []

    @property
    def all_ballots_cancelled(self):
        return all(b["cancelled"] for b in self.ballots)

    def get_cancelled_election_info(self):
        rec = {
            "cancelled": None,
            "name": None,
            "rescheduled_date": None,
            "metadata": None,
        }

        # What we care about here is if _all_
        # applicable ballot objects are cancelled.
        rec["cancelled"] = self.all_ballots_cancelled

        if not rec["cancelled"]:
            return rec

        cancelled_ballots = self.cancelled_ballots
        if cancelled_ballots:
            cancelled_ballot = cancelled_ballots[0]
            if len(cancelled_ballots) == 1:
                rec["name"] = cancelled_ballot["election_title"]
            rec["metadata"] = cancelled_ballot["metadata"]
        return rec

    @cached_property
    def cancelled_ballots(self):
        return [b for b in self.ballots if b["cancelled"]]

    def get_voter_id_status(self) -> Optional[str]:
        """
        For a given election, determine whether any ballots require photo ID
        If yes, return the stub value (e.g. EA-2022)
        If no, return None
        """
        ballot_with_id = next(
            (
                ballot
                for ballot in self.ballots
                if ballot.get("requires_voter_id") and not ballot.get("cancelled")
            ),
            {},
        )
        return ballot_with_id.get("requires_voter_id")

    def get_metadata(self):
        cancelled = self.get_cancelled_election_info()
        if cancelled["cancelled"]:
            return {"cancelled_election": cancelled["metadata"]}

        return None

    def get_ballots_for_next_date(self):
        if len(self.ballots) == 0:
            return []
        next_election_date = self._get_next_election_date()
        return [b for b in self.ballots if b["poll_open_date"] == next_election_date]

    def _get_next_election_date(self):
        # if no ballots, return early
        if len(self.ballots) == 0:
            return None
        next_charismatic_election_dates = getattr(
            settings, "NEXT_CHARISMATIC_ELECTION_DATES", []
        )
        next_charismatic_election_dates.sort()
        dates = [b["poll_open_date"] for b in self.ballots]
        dates.sort()

        if next_charismatic_election_dates:
            # If we have some dates return the first one that is in NEXT_CHARISMATIC_ELECTION_DATES
            for date in dates:
                if date in next_charismatic_election_dates:
                    return date
            # If none of them are in NEXT_CHARISMATIC_ELECTION_DATES,
            # return the earliest charismatic election date
            return next_charismatic_election_dates[0]

        # If we haven't set NEXT_CHARISMATIC_ELECTION_DATES,
        # return the earliest election
        return dates[0]

    def get_all_ballots(self):
        ballots = [
            b
            for b in self.ballots
            if b["election_id"] not in settings.ELECTION_BLACKLIST
        ]
        return sorted(ballots, key=lambda k: k["poll_open_date"])
