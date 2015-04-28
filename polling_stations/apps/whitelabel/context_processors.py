from django.conf import settings
from django.template.loader import select_template


def base_template(request):
    base_path = request.path.split('/')[1]
    if base_path in settings.EMBED_PREFIXES:
        template_name = select_template([
            '%s.html' % base_path,
            'base_embed.html',
        ])
        return {
            'base_template': template_name,
            'is_whitelabel': True,
        }
    return {
        'base_template': 'base_full.html',
    }
