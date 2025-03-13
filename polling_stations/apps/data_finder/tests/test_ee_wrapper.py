from datetime import datetime, timedelta


from data_finder.helpers.every_election import EEWrapper
from django.test import TestCase, override_settings


# mock get_data() functions
def get_data_no_elections():
    return []


def get_data_only_group():
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


def get_data_group_and_ballot():
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


def get_data_all_ballots_have_id_requirements():
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


def get_data_cancelled_ballot_has_id_requirements():
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


def get_data_some_ballots_have_id_requirements():
    return get_data_all_ballots_have_id_requirements() + get_data_group_and_ballot()


def get_data_with_elections():
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
    def test_error(self):
        ee = EEWrapper([], request_success=False)
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
    def test_no_elections(self):
        ee = EEWrapper(get_data_no_elections(), request_success=True)
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
    def test_elections(self):
        ee = EEWrapper(get_data_with_elections(), request_success=True)
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
    def test_non_charismatic_elections(self):
        # there are upcoming elections
        # but they aren't in NEXT_CHARISMATIC_ELECTION_DATES
        ee = EEWrapper(get_data_with_elections(), request_success=True)
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
    def test_elections_only_group(self):
        ee = EEWrapper(get_data_only_group(), request_success=True)
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
    def test_elections_group_and_ballot(self):
        ee = EEWrapper(get_data_group_and_ballot(), request_success=True)
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
    def test_settings_override_false(self):
        ee = EEWrapper(get_data_group_and_ballot(), request_success=True)
        # election is really happening here
        self.assertTrue(ee.has_election())
        # manually override it to false
        with override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": False}):
            ee = EEWrapper(get_data_group_and_ballot(), request_success=True)
            self.assertFalse(ee.has_election())

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": False},
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    def test_settings_override_true(self):
        ee = EEWrapper(get_data_only_group(), request_success=True)
        # election is not really happening here
        self.assertFalse(ee.has_election())
        # manually override it to true
        with override_settings(EVERY_ELECTION={"CHECK": False, "HAS_ELECTION": True}):
            ee = EEWrapper(get_data_only_group(), request_success=True)
            self.assertTrue(ee.has_election())

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        ELECTION_BLACKLIST=["foo.bar.baz.date"],
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    def test_some_blacklisted(self):
        ee = EEWrapper(get_data_with_elections(), request_success=True)
        self.assertTrue(ee.has_election())
        self.assertFalse(ee.multiple_elections)

    @override_settings(
        EVERY_ELECTION={"CHECK": True, "HAS_ELECTION": True},
        ELECTION_BLACKLIST=["foo.bar.baz.date", "foo.bar.qux.date"],
        NEXT_CHARISMATIC_ELECTION_DATES=[],
    )
    def test_all_blacklisted(self):
        ee = EEWrapper(get_data_with_elections(), request_success=True)
        self.assertFalse(ee.has_election())
        self.assertFalse(ee.multiple_elections)

    def test_get_voter_id_status_all_ballots_need_id(self):
        ee = EEWrapper(
            get_data_all_ballots_have_id_requirements(), request_success=True
        )
        status = ee.get_voter_id_status()
        self.assertEqual(status, "EA-2022")

    def test_get_voter_id_status_not_all_ballots_need_id(self):
        ee = EEWrapper(
            get_data_some_ballots_have_id_requirements(), request_success=True
        )
        status = ee.get_voter_id_status()
        status = ee.get_voter_id_status()
        self.assertEqual(status, "EA-2022")

    def test_get_voter_id_status_no_ballots_need_id(self):
        ee = EEWrapper(get_data_group_and_ballot(), request_success=True)
        status = ee.get_voter_id_status()
        self.assertEqual(status, None)

    def test_get_voter_id_status_cancelled_ballot(self):
        ee = EEWrapper(
            get_data_cancelled_ballot_has_id_requirements(), request_success=True
        )
        status = ee.get_voter_id_status()
        self.assertEqual(status, None)


def get_data_two_ballots_one_cancelled():
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


def get_data_two_ballots_both_cancelled():
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


def get_data_one_cancelled_ballot_no_replacement():
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


def get_data_one_cancelled_ballot_with_replacement():
    date1 = datetime.now().strftime("%Y-%m-%d")
    date2 = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
    return [
        {
            "election_id": "local.foo." + date1,
            "election_title": "this election",
            "group_type": None,
            "cancelled": True,
            "poll_open_date": date1,
            "replaced_by": "local.foo." + date2,
            "metadata": None,
        },
        {
            "election_id": "local.foo." + date2,
            "election_title": "that election",
            "group_type": None,
            "cancelled": False,
            "poll_open_date": date2,
            "replaced_by": None,
            "metadata": None,
        },
    ]


def get_data_one_cancelled_ballot_with_metadata():
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
    def test_two_ballots_one_cancelled(self):
        ee = EEWrapper(get_data_two_ballots_one_cancelled(), request_success=True)

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
    def test_two_ballots_both_cancelled(self):
        ee = EEWrapper(get_data_two_ballots_both_cancelled(), request_success=True)

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
    def test_one_cancelled_ballot_no_replacement(self):
        ee = EEWrapper(
            get_data_one_cancelled_ballot_no_replacement(), request_success=True
        )

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
    def test_one_cancelled_ballot_with_replacement(self):
        ee = EEWrapper(
            get_data_one_cancelled_ballot_with_replacement(), request_success=True
        )

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
    def test_one_cancelled_ballot_with_metadata(self):
        ee = EEWrapper(
            get_data_one_cancelled_ballot_with_metadata(), request_success=True
        )

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
