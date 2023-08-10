import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))


markdown_filter.is_safe = True
