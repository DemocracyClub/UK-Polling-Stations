from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sym Roe', 'sym.roe@democracyclub.org.uk'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'polling_stations',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'logger': {
            'NAME': 'ps_logger',
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'USER': '',
            'PASSWORD': ''
        }
}
DATABASE_ROUTERS = ['polling_stations.db_routers.LoggerRouter',]

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
