"""
WSGI config for  project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os
from os.path import abspath, dirname
from sys import path

import dotenv
from django.core.wsgi import get_wsgi_application

SITE_ROOT = dirname(dirname(abspath(__file__)))
path.append(SITE_ROOT)

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polling_stations.settings")


application = get_wsgi_application()
