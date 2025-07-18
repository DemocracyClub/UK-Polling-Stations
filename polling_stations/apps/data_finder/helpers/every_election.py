import abc
import datetime
from typing import List, Optional
from urllib.parse import urlencode, urljoin

import requests
from dateutil.parser import parse
from django.conf import settings
from django.core.cache import cache
from uk_geo_utils.helpers import Postcode


class EEFetcher:
    def __init__(self, postcode=None, point=None, council_id=None):
        # always request "current" elections
        # it is the responsibility of EEWrapper to filter to future
        self.base_params = {"identifier_type": "ballot", "current": 1}
        if not any((postcode, point, council_id)):
            raise ValueError("Expected either a point, postcode or council_id")
        self.postcode = postcode
        self.point = point
        self.council_id = council_id
        self.postcode = postcode

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

            res = requests.get(query_url, timeout=10, headers=headers)

            if res.status_code != 200:
                res.raise_for_status()

            res_json = res.json()
            if cache_hours:
                cache.set(query_url, res_json, 60 * 60 * cache_hours)

        if "results" in res_json:
            return res_json["results"]
        return res_json

    def fetch(self):
        request_success = False
        elections = []
        try:
            if self.postcode:
                elections = self.get_data_by_postcode(
                    Postcode(self.postcode).with_space
                )
                request_success = True
            if self.point:
                elections = self.get_data_by_point(self.point)
                request_success = True
            if self.council_id:
                elections = self.get_election_intersecting_local_authority(
                    self.council_id
                )
                request_success = True
        except requests.exceptions.RequestException:
            request_success = False

        return {"elections": elections, "request_success": request_success}


# if we're adding a "public" property, add it to the BaseEEWrapper
# and implement it in both implementations


class BaseEEWrapper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def has_election(self, future_only=True) -> bool:
        pass

    @abc.abstractmethod
    def get_metadata(self):
        pass

    @abc.abstractmethod
    def get_next_election_date(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_ballots_for_next_date(self) -> List:
        pass

    @abc.abstractmethod
    def get_all_ballots(self) -> List:
        pass

    @property
    @abc.abstractmethod
    def multiple_elections(self):
        pass

    @abc.abstractmethod
    def get_explanations(self):
        pass

    @abc.abstractmethod
    def get_voter_id_status(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def get_cancelled_election_info(self):
        pass

    @property
    @abc.abstractmethod
    def has_city_of_london_ballots(self) -> bool:
        pass


class EmptyEEWrapper(BaseEEWrapper):
    def has_election(self, future_only=True) -> bool:
        return False

    def get_metadata(self) -> None:
        return None

    def get_next_election_date(self) -> Optional[str]:
        return None

    def get_ballots_for_next_date(self) -> List:
        return []

    def get_all_ballots(self) -> List:
        return []

    @property
    def multiple_elections(self):
        return False

    def get_explanations(self):
        return []

    def get_voter_id_status(self) -> Optional[str]:
        return None

    def get_cancelled_election_info(self):
        return {}

    @property
    def has_city_of_london_ballots(self) -> bool:
        return False


class EEWrapper(BaseEEWrapper):
    def __init__(self, elections, request_success, include_current=False):
        self.elections = elections
        if not include_current:
            self.elections = [
                e
                for e in self.elections
                if datetime.datetime.strptime(e["poll_open_date"], "%Y-%m-%d").date()
                >= datetime.datetime.today().date()
            ]
        self.request_success = request_success
        self.ballots = self.get_ballots_for_next_date()
        self.cancelled_ballots = self.get_cancelled_ballots()

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

    def get_next_election_date(self):
        ballots = self.get_all_ballots()
        # if no ballots, return early
        if len(ballots) == 0:
            return None

        dates = [b["poll_open_date"] for b in ballots]
        dates.sort()

        return dates[0]

    def get_ballots_for_next_date(self):
        if not self.request_success:
            return []
        ballots = self.get_all_ballots()
        if len(ballots) == 0:
            return ballots
        next_election_date = self.get_next_election_date()
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
            rec["rescheduled_date"] = datetime.datetime.strptime(
                cancelled_ballot["replaced_by"].split(".")[-1], "%Y-%m-%d"
            ).strftime("%-d %B %Y")

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
                    and election["poll_open_date"] == self.get_next_election_date()
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
        if self.has_election() and self.request_success:
            uncancelled_ballots = [b for b in self.ballots if not b["cancelled"]]
            return len(uncancelled_ballots) > 1
        return False

    @property
    def has_city_of_london_ballots(self):
        # City of London local elections have some edge cases e.g:
        # diffrent polling station opening times, different registration rules
        if not self.request_success:
            return False
        uncancelled_ballots = [b for b in self.ballots if not b["cancelled"]]
        for b in uncancelled_ballots:
            if b["election_id"].startswith("local.city-of-london"):
                return True
        return False
