from django.apps import apps
from django.conf import settings
from django.core.checks import Error, Info, register


@register()
def mapquest_sdk_check(app_configs, **kwargs):
    errors = []

    if app_configs is None or apps.get_app_config("data_finder") in app_configs:

        if settings.TILE_LAYER == "MapQuestSDK" and settings.MQ_KEY is None:
            errors.append(
                Error(
                    "TILE_LAYER is 'MapQuestSDK' but no MapQuest API Key is set",
                    hint="Define MQ_KEY as an env var or in local.py",
                    obj="data_finder",
                    id="data_finder.E001",
                )
            )
    return errors


@register()
def google_api_check(app_configs, **kwargs):
    errors = []

    if app_configs is None or apps.get_app_config("data_finder") in app_configs:

        if settings.GOOGLE_API_KEY == "":
            errors.append(
                Info(
                    "Google API Key is not set - usage limits will apply",
                    hint="Define GOOGLE_API_KEY as an env var or in local.py",
                    obj="data_finder",
                    id="data_finder.I002",
                )
            )
    return errors
