from data_finder.helpers import ExamplePostcodeHelper


def example_postcode_context(request):
    return {'example_postcode': ExamplePostcodeHelper()}
