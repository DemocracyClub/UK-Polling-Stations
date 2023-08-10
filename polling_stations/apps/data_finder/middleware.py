class UTMTrackerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        def _get_value_from_req(key):
            return (key, request.GET.get(key, None))

        keys = ("utm_source", "utm_medium", "utm_campaign")
        utm_data = {k: v for k, v in map(_get_value_from_req, keys) if v}
        request.session["utm_data"] = utm_data
