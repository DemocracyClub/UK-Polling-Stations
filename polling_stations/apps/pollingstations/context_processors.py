from django.conf import settings


def google_analytics(request):
    return {"disable_ga": getattr(settings, "DISABLE_GA", False)}


def global_settings(request):
    return {
        "RAVEN_CONFIG": getattr(settings, "RAVEN_CONFIG", None),
        "SERVER_ENVIRONMENT": getattr(settings, "SERVER_ENVIRONMENT", None),
    }
