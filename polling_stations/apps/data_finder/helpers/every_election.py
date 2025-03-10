def EveryElectionWrapper(
    postcode=None, point=None, council_id=None, include_current=False
):
    from .ee2 import EEFetcher, EEWrapper

    kwargs = EEFetcher(postcode, point, council_id).fetch()
    kwargs["include_current"] = include_current

    return EEWrapper(**kwargs)


def EmptyEveryElectionWrapper():
    from .ee2 import EmptyEEWrapper

    return EmptyEEWrapper()


def StaticElectionsAPIElectionWrapper(elections_response, include_current=False):
    from .ee2 import EEWrapper

    return EEWrapper(
        elections_response["ballots"],
        request_success=elections_response["request_success"],
        include_current=include_current,
    )
