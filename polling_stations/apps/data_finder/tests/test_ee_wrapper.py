from datetime import datetime, timedelta
from urllib.parse import parse_qs

import mock
import requests
from django.test import TestCase, override_settings
from data_finder.helpers import EveryElectionWrapper


# mock get_data() functions
def get_data_exception(self, query_url):
    raise requests.exceptions.RequestException()


def get_data_no_elections(self, query_url):
    return []


def get_data_only_group(self, query_url):
    return [
        {
            "election_id": "foo.date",
            "election_title": "some election",
            "group_type": "election",
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
        {
            "election_id": "foo.bar.date",
            "election_title": "some election",
            "group_type": "organisation",
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
    ]


def get_data_group_and_ballot(self, query_url):
    return [
        {
            "election_id": "foo.bar.date",
            "election_title": "some election",
            "group_type": "organisation",
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
    ]


def get_data_all_ballots_have_id_requirements(self, query_url):
    return [
        {
            "election_id": f"foo.bar.baz.{(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')}",
            "election_title": "some election",
            "group_type": None,
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "requires_voter_id": "EA-2022",
        }
    ]


def get_data_cancelled_ballot_has_id_requirements(self, query_url):
    return [
        {
            "election_id": f"foo.bar.baz.{(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')}",
            "election_title": "some election",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "requires_voter_id": "EA-2022",
        }
    ]


def get_data_some_ballots_have_id_requirements(self, query_url):
    ballots = get_data_all_ballots_have_id_requirements(
        self, query_url
    ) + get_data_group_and_ballot(self, query_url)
    return ballots


def get_data_with_elections(self, query_url):
    return [
        {
            "election_id": "foo.bar.date",
            "election_title": "some election",
            "group_type": "organisation",
            "metadata": None,
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },  # no explanation or metadata keys
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "explanation": None,
            "metadata": None,
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },  # null explanation and metadata keys
        {
            "election_id": "foo.bar.qux.date",
            "election_title": "some election",
            "group_type": None,
            "explanation": "some text",  # explanation key contains text
            "cancelled": False,
            "poll_open_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        },
    ]


class EveryElectionWrapperTests(TestCase):
    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_exception)
    def test_exception(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertFalse(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([], ee.get_explanations())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(None, ee.get_metadata())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_no_elections
    )
    def test_no_elections(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(None, ee.get_metadata())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections
    )
    def test_elections(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual(
            [{"title": "some election", "explanation": "some text"}],
            ee.get_explanations(),
        )
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertTrue(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[
            (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        ],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections
    )
    def test_non_charismatic_elections(self):
        # there are upcoming elections
        # but they aren't in NEXT_CHARISMATIC_ELECTION_DATES
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(None, ee.get_metadata())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_only_group
    )
    def test_elections_only_group(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(None, ee.get_metadata())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_group_and_ballot
    )
    def test_elections_group_and_ballot(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([], ee.get_explanations())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(None, ee.get_metadata())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": False},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_group_and_ballot
    )
    def test_settings_override_false(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        # election is really happening here
        self.assertTrue(ee.has_election())
        # manually override it to false
        with override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": False}):
            ee = EveryElectionWrapper(postcode="AA11AA")
            self.assertFalse(ee.has_election())

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": False},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_only_group
    )
    def test_settings_override_true(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        # election is not really happening here
        self.assertFalse(ee.has_election())
        # manually override it to true
        with override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": True}):
            ee = EveryElectionWrapper(postcode="AA11AA")
            self.assertTrue(ee.has_election())

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        ELECTION_BLACKLIST=["foo.bar.baz.date"],
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections
    )
    def test_some_blacklisted(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        ELECTION_BLACKLIST=["foo.bar.baz.date", "foo.bar.qux.date"],
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections
    )
    def test_all_blacklisted(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertFalse(ee.multiple_elections)

    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_all_ballots_have_id_requirements,
    )
    def test_get_voter_id_status_all_ballots_need_id(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        status = ee.get_voter_id_status()
        self.assertEqual(status, "EA-2022")

    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_some_ballots_have_id_requirements,
    )
    def test_get_voter_id_status_not_all_ballots_need_id(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        status = ee.get_voter_id_status()
        self.assertEqual(status, "EA-2022")

    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data", get_data_group_and_ballot
    )
    def test_get_voter_id_status_no_ballots_need_id(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        status = ee.get_voter_id_status()
        self.assertEqual(status, None)

    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_cancelled_ballot_has_id_requirements,
    )
    def test_get_voter_id_status_cancelled_ballot(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        status = ee.get_voter_id_status()
        self.assertEqual(status, None)


def get_data_two_ballots_one_cancelled(self, query_url):
    # 2 ballots on the same date
    # one is cancelled, one isn't
    return [
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
        },
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "cancelled": False,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
        },
    ]


def get_data_two_ballots_both_cancelled(self, query_url):
    # 2 different ballots on the same date
    # both are cancelled
    return [
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election 1",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
            "metadata": None,
        },
        {
            "election_id": "qux.bar.date",
            "election_title": "some election 2",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
            "metadata": None,
        },
    ]


def get_data_one_cancelled_ballot_no_replacement(self, query_url):
    return [
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
            "metadata": None,
        }
    ]


def get_data_one_cancelled_ballot_with_replacement(self, query_url):
    this_election = {
        "election_id": "local.foo.thisdate",
        "election_title": "this election",
        "group_type": None,
        "cancelled": True,
        "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
        "replaced_by": "local.foo.thatdate",
        "metadata": None,
    }
    that_election = {
        "election_id": "local.foo.thatdate",
        "election_title": "that election",
        "group_type": None,
        "cancelled": False,
        "poll_open_date": (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d"),
        "replaced_by": None,
        "metadata": None,
    }
    query_params = parse_qs(query_url.split("?")[-1])
    expected_params = {
        "postcode": ["AA1 1AA"],
        "future": ["1"],
        "current": ["1"],
        "identifier_type": ["ballot"],
    }
    if query_params == expected_params:
        return [this_election, that_election]
    if query_url.endswith("/api/elections/local.foo.thatdate.json"):
        return that_election
    raise Exception(f"no fixture match for {query_url=}")


def get_data_one_cancelled_ballot_with_metadata(self, query_url):
    return [
        {
            "election_id": "foo.bar.baz.date",
            "election_title": "some election",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": datetime.now().strftime("%Y-%m-%d"),
            "replaced_by": None,
            "metadata": {
                "cancelled_election": {
                    "detail": "Oh noes! Terrible things happened to this election. [more info](http://foo.bar/baz)"
                }
            },
        }
    ]


class CancelledElectionTests(TestCase):
    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_two_ballots_one_cancelled,
    )
    def test_two_ballots_one_cancelled(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election(future_only=False))
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], False)
        self.assertEqual(cancelled_info["name"], None)
        self.assertEqual(cancelled_info["rescheduled_date"], None)
        self.assertEqual(cancelled_info["metadata"], None)
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_two_ballots_both_cancelled,
    )
    def test_two_ballots_both_cancelled(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], True)
        self.assertEqual(cancelled_info["name"], None)
        self.assertEqual(cancelled_info["rescheduled_date"], None)
        self.assertEqual(cancelled_info["metadata"], None)
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_one_cancelled_ballot_no_replacement,
    )
    def test_one_cancelled_ballot_no_replacement(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], True)
        self.assertEqual(cancelled_info["name"], "some election")
        self.assertEqual(cancelled_info["rescheduled_date"], None)
        self.assertEqual(cancelled_info["metadata"], None)
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_one_cancelled_ballot_with_replacement,
    )
    def test_one_cancelled_ballot_with_replacement(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], True)
        self.assertEqual(cancelled_info["name"], "this election")
        self.assertEqual(
            cancelled_info["rescheduled_date"],
            (datetime.now() + timedelta(weeks=1)).strftime("%-d %B %Y"),
        )
        self.assertEqual(cancelled_info["metadata"], None)
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    @mock.patch(
        "data_finder.helpers.EveryElectionWrapper.get_data",
        get_data_one_cancelled_ballot_with_metadata,
    )
    def test_one_cancelled_ballot_with_metadata(self):
        ee = EveryElectionWrapper(postcode="AA11AA")
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        cancelled_info = ee.get_cancelled_election_info()
        self.assertEqual(cancelled_info["cancelled"], True)
        self.assertEqual(cancelled_info["name"], "some election")
        self.assertEqual(cancelled_info["rescheduled_date"], None)
        self.assertTrue(
            "Oh noes!" in cancelled_info["metadata"]["cancelled_election"]["detail"]
        )
        self.assertTrue("cancelled_election" in ee.get_metadata())
        self.assertFalse(ee.multiple_elections)
