class EEMock:
    def get_metadata(self):
        return None


class EEMockWithElection(EEMock):
    def has_election(self):
        return True


class EEMockWithoutElection(EEMock):
    def has_election(self):
        return False
