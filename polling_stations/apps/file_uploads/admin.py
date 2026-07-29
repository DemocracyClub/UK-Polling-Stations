from core.admin_mixins import ReadOnlyModelAdminMixin
from django.contrib import admin
from file_uploads.models import FcsCredential, File, Upload


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


@admin.register(FcsCredential)
class FcsCredentialAdmin(admin.ModelAdmin):
    list_display = ["council", "url"]
    search_fields = ["council__name", "url"]
