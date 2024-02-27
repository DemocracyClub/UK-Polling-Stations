from core.admin_mixins import ReadOnlyModelAdminMixin
from django.contrib import admin
from file_uploads.models import File, Upload


class FileInline(admin.StackedInline):
    model = File
    extra = 0


class UploadAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    inlines = [FileInline]
    search_fields = [
        "election_date",
        "github_issue",
        "timestamp",
        "gss__name",
    ]


admin.site.register(Upload, UploadAdmin)
