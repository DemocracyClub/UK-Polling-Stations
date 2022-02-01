from django.conf import settings
from django.db import DEFAULT_DB_ALIAS


class LoggerRouter(object):

    logger_apps = [
        "admin",
        "auth",
        "authtoken",
        "bug_reports",
        "contenttypes",
        "data_finder",
        "feedback",
        "file_uploads",
    ]

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.logger_apps:
            return settings.LOGGER_DB_NAME
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.logger_apps:
            return settings.LOGGER_DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "councils" or obj2._meta.app_label == "councils":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.logger_apps:
            return db == settings.LOGGER_DB_NAME
        return None


def get_logger_db_name():
    if settings.LOGGER_DB_NAME in settings.DATABASES.keys() and not getattr(
        settings, "RUNNING_TESTS", False
    ):
        return settings.LOGGER_DB_NAME
    return DEFAULT_DB_ALIAS
