import os

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django_middleware_global_request import get_request


PRIMARY = settings.PRINCIPAL_DB_NAME
REPLICA = DEFAULT_DB_ALIAS


class ReplicationRouter(object):
    def db_for_read(self, model, **hints):
        # In CI, there is only one DB connection
        if os.environ.get("CIRCLECI"):
            return DEFAULT_DB_ALIAS

        # We don't need to scale requests touching these models
        # but we do want to prevent race conditions
        # when reading a record we just wrote
        if model._meta.label in (
            "file_uploads.Upload",
            "file_uploads.File",
        ):
            return PRIMARY

        # We only care about trying to scale
        # by serving traffic from a replica
        # when we are serving HTTP traffic
        request = get_request()
        if request:
            if request.path.startswith("/admin"):
                return PRIMARY
            return REPLICA

        # in all other cases (e.g: management commands, shell)
        # perform reads from the primary to prevent race conditions
        return PRIMARY

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
