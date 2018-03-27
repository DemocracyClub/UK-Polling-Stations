from django.contrib import admin
from .models import LoggedPostcode


class LoggedPostcodeAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'postcode',
        'had_data',
        'council',
        'brand',
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'language',
        'view_used',
        'api_user',
    )
    readonly_fields = [f.name for f in LoggedPostcode._meta.get_fields()]
    ordering = ('-created', 'id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LoggedPostcode, LoggedPostcodeAdmin)
