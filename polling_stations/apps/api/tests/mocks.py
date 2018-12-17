class EEMock:
    def get_metadata(self):
        return None


class EEMockWithElection(EEMock):
    def has_election(self):
        return True

    def get_all_ballots(self):
        return [
            {
                "election_id": "local.foo-town.2018-05-03",
                "election_title": "Foo Town Local Election: Bar Ward",
                "poll_open_date": "2018-05-03",
                "elected_role": "Local Councillor",
                "metadata": None,
                "cancelled": False,
                "replaced_by": None,
                "replaces": None,
            }
        ]

    def get_ballots_for_next_date(self):
        return [
            {
                "election_id": "local.foo-town.2018-05-03",
                "election_title": "Foo Town Local Election: Bar Ward",
                "poll_open_date": "2018-05-03",
                "elected_role": "Local Councillor",
                "metadata": None,
                "cancelled": False,
                "replaced_by": None,
                "replaces": None,
            }
        ]


class EEMockWithoutElection(EEMock):
    def has_election(self):
        return False

    def get_all_ballots(self):
        return []

    def get_ballots_for_next_date(self):
        return []
