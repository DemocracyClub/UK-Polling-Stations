from django import template
from file_uploads.models import UploadStatusChoices

register = template.Library()


@register.filter(name="upload_status_emoji")
def upload_status_emoji(status_value):
    try:
        return UploadStatusChoices[status_value].label
    except KeyError:
        return status_value
