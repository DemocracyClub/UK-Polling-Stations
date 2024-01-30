import os

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS


class ReplicationRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.label in (
            "file_uploads.Upload",
            "file_uploads.File",
        ) and not os.environ.get("CIRCLECI"):
            return settings.PRINCIPAL_DB_NAME
        return DEFAULT_DB_ALIAS

    def db_for_write(self, model, **hints):
        if os.environ.get("CIRCLECI"):
            return DEFAULT_DB_ALIAS
        return settings.PRINCIPAL_DB_NAME

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


def get_principal_db_name():
    if settings.PRINCIPAL_DB_NAME in settings.DATABASES:
        return settings.PRINCIPAL_DB_NAME
    return DEFAULT_DB_ALIAS
