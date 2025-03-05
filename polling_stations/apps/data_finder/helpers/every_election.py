def EveryElectionWrapper(
    postcode=None, point=None, council_id=None, include_current=False
):
    from .ee2 import EEFetcher, EEWrapper

    return EEWrapper(**EEFetcher(postcode, point, council_id, include_current).fetch())


def EmptyEveryElectionWrapper():
    from .ee2 import EmptyEEWrapper

    return EmptyEEWrapper()


def StaticElectionsAPIElectionWrapper(elections_response):
    from .ee2 import EEWrapper

    return EEWrapper(elections_response["ballots"], True)
