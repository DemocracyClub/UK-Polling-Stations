from django.conf import settings
from django.core.urlresolvers import set_script_prefix
from django.utils import translation


class WhiteLabelMiddleware(object):
    def process_request(self, request):
        base_path = request.path.split('/')[1]
        request.brand = "democracyclub"
        if base_path in settings.EMBED_PREFIXES:
            request.brand = base_path
            set_script_prefix("/%s" % base_path)
        if base_path in settings.WHITELABEL_PREFIXES:
            request.brand = base_path
        if request.brand == 'nus_wales':
            if request.GET.get('lang', '') == 'en':
                request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
                translation.activate('en')
            if request.GET.get('lang', '') == 'cy':
                request.session[translation.LANGUAGE_SESSION_KEY] = 'cy-gb'
                translation.activate('cy-gb')

    def process_response(self, request, response):
        base_path = request.path.split('/')[1]
        if base_path in settings.EMBED_PREFIXES:
            if 'X-Frame-Options' in response:
                del response['X-Frame-Options']
        return response
