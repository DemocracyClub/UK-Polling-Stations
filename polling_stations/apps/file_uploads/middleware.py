class NoCacheMiddleware:
    """
    Serve every response from the file_uploads app with no-cache headers.
    """

    CACHE_CONTROL = "max-age=0, no-cache, no-store, must-revalidate, private"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        match = getattr(request, "resolver_match", None)
        if match and "file_uploads" in match.app_names:
            response["Cache-Control"] = self.CACHE_CONTROL
        return response
