APPS_THAT_USE_LOGGER = [
    'data_finder',
    'data_collection',
]

class LoggerRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label in APPS_THAT_USE_LOGGER :
            return 'logger'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in APPS_THAT_USE_LOGGER:
            return 'logger'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'councils' or \
           obj2._meta.app_label == 'councils':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in APPS_THAT_USE_LOGGER:
            return db == 'logger'
        return None
