from django.core.management.commands.compilemessages import Command as BaseCommand


class Command(BaseCommand):
    # We override this to disable errors when a translator translates "%(council)s"
    # as "%(council_aspirate)s". However, unintentional errors will not be caught,
    # so we will need to watch for TemplateSyntaxError from the {% blocktrans[late] %}
    # tag.
    program_options = []
