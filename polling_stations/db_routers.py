class LoggerRouter(object):

    logger_apps = ['data_finder', 'admin', 'auth', 'authtoken']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.logger_apps:
            return 'logger'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.logger_apps:
            return 'logger'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'councils' or \
           obj2._meta.app_label == 'councils':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.logger_apps:
            return db == 'logger'
        return None
