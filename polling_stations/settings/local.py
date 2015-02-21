from .base import *


ADMINS = (
    ('Sym Roe', 'sym.roe@democracyclub.org.uk'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pollingstations',
        'USER': 'symroe',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
