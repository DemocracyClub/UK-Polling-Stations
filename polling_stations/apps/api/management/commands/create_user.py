from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--username',
            help='username',
            required=True
        )

        parser.add_argument(
            '-p',
            '--password',
            help='password',
            required=True
        )

        parser.add_argument(
            '-e',
            '--email',
            help='email',
            required=True
        )

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(
            kwargs['username'], kwargs['email'], kwargs['password'])
        token = Token.objects.create(user=user)
        print(token.key)
