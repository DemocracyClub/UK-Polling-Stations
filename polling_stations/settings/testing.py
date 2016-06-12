from .base import *

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('aloe_django',)

NOSE_ARGS = [
    '--nocapture',
    '--verbosity=0',
    '--nologcapture',
]

MIGRATION_MODULES = {
    app.split('.')[-1]: '{}.nomigrations'.format(
        app.split('.')[-1])
    for app in INSTALLED_APPS
    if 'django' not in app
}
