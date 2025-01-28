import os

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS

PRIMARY = settings.PRINCIPAL_DB_NAME
REPLICA = DEFAULT_DB_ALIAS


class ReplicationRouter(object):
    def db_for_read(self, model, **hints):
        if os.environ.get("CIRCLECI"):
            return DEFAULT_DB_ALIAS

        if model._meta.label in (
            "file_uploads.Upload",
            "file_uploads.File",
        ):
            return PRIMARY
        return REPLICA

    def db_for_write(self, model, **hints):
        if os.environ.get("CIRCLECI"):
            return DEFAULT_DB_ALIAS

        return PRIMARY

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


def get_principal_db_name():
    if PRIMARY in settings.DATABASES:
        return PRIMARY
    return REPLICA
