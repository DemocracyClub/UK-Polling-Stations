from django.conf import settings


def google_analytics(request):
    return {
        'disable_ga': getattr(settings, 'DISABLE_GA', False)
    }
