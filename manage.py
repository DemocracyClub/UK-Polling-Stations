#!/usr/bin/env python
import os
import sys
import warnings

import dotenv

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polling_stations.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
