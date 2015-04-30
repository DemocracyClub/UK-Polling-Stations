from django.conf import settings
from django.core.urlresolvers import set_script_prefix


class WhiteLabelModdleware(object):
    def process_request(self, request):
        base_path = request.path.split('/')[1]
        if base_path in settings.EMBED_PREFIXES:
            set_script_prefix("/%s" % base_path)

    def process_response(self, request, response):
        base_path = request.path.split('/')[1]
        if base_path in settings.EMBED_PREFIXES:
            if 'X-Frame-Options' in response:
                del response['X-Frame-Options']
        return response