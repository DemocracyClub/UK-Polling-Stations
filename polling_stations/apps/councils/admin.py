from core.admin_mixins import ReadOnlyModelAdminMixin
from councils.models import Council
from django.contrib import admin


class CouncilUserInline(admin.StackedInline):
    model = Council.users.through
    extra = 0


class CouncilAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    inlines = [CouncilUserInline]
    search_fields = ["council_id", "name", "identifiers"]


admin.site.register(Council, CouncilAdmin)
