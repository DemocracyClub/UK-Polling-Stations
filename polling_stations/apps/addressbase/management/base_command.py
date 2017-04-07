from django.apps import apps
from django.core.management.base import BaseCommand


class BaseAddressBaseCommand(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'addressbase' and 'pollingstations' apps
    """
    requires_system_checks = False

    def perform_checks(self):
        """
        Manually run system checks for the
        'addressbase' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('addressbase'),
            apps.get_app_config('pollingstations')
        ])
