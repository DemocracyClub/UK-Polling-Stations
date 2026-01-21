"""
A django DB backend that throws an error if you try to do anything. This is
useful for testing database routing. We can use it if we want to configure a
DB connection and ensure that it was definitely not used.

Based on
https://github.com/django/django/tree/main/django/db/backends/dummy
"""

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.dummy.features import DummyDatabaseFeatures


def complain(*args, **kwargs):
    raise AssertionError("DB Connection accessed unexpectedly")


def ignore(*args, **kwargs):
    pass


class DatabaseOperations(BaseDatabaseOperations):
    quote_name = complain


class DatabaseClient(BaseDatabaseClient):
    runshell = complain


class DatabaseCreation(BaseDatabaseCreation):
    create_test_db = ignore
    destroy_test_db = ignore


class DatabaseIntrospection(BaseDatabaseIntrospection):
    get_table_list = complain
    get_table_description = complain
    get_relations = complain
    get_indexes = complain


class DatabaseWrapper(BaseDatabaseWrapper):
    operators = {}
    # Override the base class implementations with null
    # implementations. Anything that tries to actually
    # do something raises complain
    _cursor = complain
    ensure_connection = ignore
    _commit = complain
    _rollback = complain
    _close = complain
    _savepoint = complain
    _savepoint_commit = complain
    _savepoint_rollback = complain
    _set_autocommit = complain
    # Classes instantiated in __init__().
    client_class = DatabaseClient
    creation_class = DatabaseCreation
    features_class = DummyDatabaseFeatures
    introspection_class = DatabaseIntrospection
    ops_class = DatabaseOperations

    def is_usable(self):
        return True
