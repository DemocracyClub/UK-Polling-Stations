import csv
import datetime

from core.admin_mixins import AsanaUrlExistsFilter, send_to_asana
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import re_path
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.safestring import mark_safe

from .models import BugReport


def resolve(modeladmin, request, queryset):
    queryset.update(status="RESOLVED")


resolve.short_description = "Mark selected issues as Resolved"


class BugReportAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "source_url", "description", "source")
    list_filter = (AsanaUrlExistsFilter,)
    readonly_fields = [
        f.name
        for f in BugReport._meta.get_fields()
        if f.name not in ["status", "report_type"]
    ] + ["preview_url"]
    ordering = ("status", "-created", "id")
    actions = [resolve, send_to_asana]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def preview_url(self, obj):
        if obj.source == "wheredoivote" and url_has_allowed_host_and_scheme(
            obj.source_url, allowed_hosts=None
        ):
            link = self.request.build_absolute_uri(obj.source_url)
            return mark_safe('<a href="%s">%s</a>' % (link, link))
        return "-"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            re_path("export_all/", self.export_all),
            re_path("export_open/", self.export_open),
        ]
        return my_urls + urls

    def export_all(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied")
        return self.export(BugReport.objects.all().order_by("status", "-created", "id"))

    def export_open(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied")
        return self.export(
            BugReport.objects.all()
            .filter(status="OPEN")
            .order_by("status", "-created", "id")
        )

    def export(self, qs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="bug-reports-%s.csv"'
            % (datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S"))
        )
        fields = [f.name for f in BugReport._meta.get_fields()]
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in qs:
            writer.writerow([getattr(row, field) for field in fields])
        return response


admin.site.register(BugReport, BugReportAdmin)
