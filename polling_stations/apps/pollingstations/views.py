import os
from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpResponse


def status_check(request):

    if settings.CHECK_SERVER_CLEAN:
        if not os.path.exists(os.path.expanduser(settings.CLEAN_SERVER_FILE)):
            return HttpResponse("service unavailable", status=503)

    # check we can connect to all our DBs
    # (default + logger)
    for conn in connections:
        try:
            connections[conn].cursor()
        except OperationalError:
            return HttpResponse("service unavailable", status=503)

    return HttpResponse("OK", status=200)
