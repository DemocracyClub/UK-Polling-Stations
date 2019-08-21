from datetime import datetime, timedelta
import requests
from django.conf import settings
from uk_geo_utils.helpers import Postcode


class EveryElectionWrapper:
    def __init__(self, postcode=None, point=None):
        if not postcode and not point:
            raise ValueError("Expected either a point or a postcode")
        try:
            self.request_success = False
            if postcode:
                self.elections = self.get_data_by_postcode(
                    Postcode(postcode).with_space
                )
                self.request_success = True
            elif point:
                self.elections = self.get_data_by_point(point)
                self.request_success = True
            self.ballots = self.get_ballots_for_next_date()
            self.cancelled_ballots = self.get_cancelled_ballots()
        except requests.exceptions.RequestException:
            self.request_success = False

    def get_data_by_postcode(self, postcode):
        query_url = "%sapi/elections.json?postcode=%s&future=1" % (
            settings.EE_BASE,
            postcode,
        )
        return self.get_data(query_url)

    def get_data_by_point(self, point):
        query_url = "%sapi/elections.json?coords=%s,%s&future=1" % (
            settings.EE_BASE,
            point.y,
            point.x,
        )
        return self.get_data(query_url)

    def get_data(self, query_url):
        headers = {}
        if hasattr(settings, "CUSTOM_UA"):
            headers["User-Agent"] = settings.CUSTOM_UA

        res = requests.get(query_url, timeout=4, headers=headers)

        if res.status_code != 200:
            res.raise_for_status()

        res_json = res.json()
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

    def _get_next_election_date(self):
        ballots = self.get_all_ballots()
        next_charismatic_election_date = getattr(
            settings, "NEXT_CHARISMATIC_ELECTION_DATE", None
        )
        if len(ballots) == 0:
            return next_charismatic_election_date
        dates = [datetime.strptime(b["poll_open_date"], "%Y-%m-%d") for b in ballots]
        dates.sort()
        return (
            next_charismatic_election_date
            if next_charismatic_election_date
            else dates[0].strftime("%Y-%m-%d")
        )

    def get_ballots_for_next_date(self):
        if not self.request_success:
            return []
        ballots = self.get_all_ballots()
        if len(ballots) == 0:
            return ballots
        next_election_date = self._get_next_election_date()
        ballots = [e for e in ballots if e["poll_open_date"] == next_election_date]
        return ballots

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

        if len(self.cancelled_ballots) > 1:
            # If there were 2 or more elections scheduled to happen
            # on this day and all of them got cancelled
            # its diffuclt to know how to present this info in the abstract
            # lets just say something generic
            return rec

        # there is exactly one cancelled election
        cancelled_ballot = self.cancelled_ballots[0]
        rec["name"] = cancelled_ballot["election_title"]
        rec["metadata"] = cancelled_ballot["metadata"]

        if cancelled_ballot["replaced_by"]:
            try:
                query_url = "%sapi/elections/%s.json" % (
                    settings.EE_BASE,
                    cancelled_ballot["replaced_by"],
                )
                new_ballot = self.get_data(query_url)
                rec["rescheduled_date"] = datetime.strptime(
                    new_ballot["poll_open_date"], "%Y-%m-%d"
                ).strftime("%-d %B %Y")
            except requests.exceptions.RequestException:
                rec["rescheduled_date"] = None

        return rec

    def has_election(self):
        if not settings.EVERY_ELECTION["CHECK"]:
            return settings.EVERY_ELECTION["HAS_ELECTION"]

        if not self.request_success:
            # if the request was unsuccessful for some reason,
            # assume there *is* an upcoming election
            return True

        if len(self.ballots) > 0 and not self.all_ballots_cancelled:
            if not settings.EVERY_ELECTION["THRESHOLD_DAYS"]:
                return True
            if (
                datetime.strptime(self._get_next_election_date(), "%Y-%m-%d")
                - timedelta(days=settings.EVERY_ELECTION["THRESHOLD_DAYS"])
                <= datetime.now()
            ):
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

        # merge Voter id pilot in England and
        # Standard Northern Ireland ID requirement
        # in the API outputs
        voter_id = self.get_id_pilot_info() or self.get_metadata_by_key("ni-voter-id")
        if voter_id:
            return {"voter_id": voter_id}

        return None

    def get_metadata_by_key(self, key):
        if not settings.EVERY_ELECTION["CHECK"] or not self.request_success:
            return None

        for b in self.ballots:
            if "metadata" in b and b["metadata"] and key in b["metadata"]:
                return b["metadata"][key]
        return None

    def get_id_pilot_info(self):
        return self.get_metadata_by_key("2019-05-02-id-pilot")
