from .base import *

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('aloe_django',)

NOSE_ARGS = [
    '--verbosity=0',
    '--nologcapture',
]

MIGRATION_MODULES = {
    app: '{}.nomigrations'.format(app)
    for app in INSTALLED_APPS
    if 'django' not in app
}
