from django.contrib import admin

from core.admin_mixins import ReadOnlyModelAdminMixin
from file_uploads.models import Upload, File


class FileInline(admin.StackedInline):
    model = File
    extra = 0


class UploadAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    inlines = [FileInline]
    search_fields = ["gss", "election_date", "github_issue", "timestamp"]


admin.site.register(Upload, UploadAdmin)
