from django.conf import settings
from django.urls import set_script_prefix
from django.utils import translation


class WhiteLabelMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.process_response(
            request, self.get_response(request))
        return response

    def process_request(self, request):
        base_path = request.path.split('/')[1]
        request.brand = "democracyclub"
        if base_path in settings.EMBED_PREFIXES:
            request.brand = base_path
            set_script_prefix("/%s" % base_path)
        if base_path in settings.WHITELABEL_PREFIXES:
            request.brand = base_path

    def process_response(self, request, response):
        base_path = request.path.split('/')[1]
        if base_path in settings.EMBED_PREFIXES:
            if 'X-Frame-Options' in response:
                del response['X-Frame-Options']
        return response
