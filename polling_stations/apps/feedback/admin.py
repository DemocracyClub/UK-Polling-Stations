import csv
import datetime
import re

from core.admin_mixins import AsanaUrlExistsFilter, send_to_asana
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import re_path
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.safestring import mark_safe

from .models import Feedback, NoElectionFeedback


def check_source_url_for_preview(source_url):
    pattern = re.compile(
        r"""
            ^            # Start of string
            /address/    # "/address/"
            [^/]+        # One or more characters that are not a forward slash
            /            # "/"
        |                # OR
            /postcode/   # "/postcode/"
            [^/]+        # One or more characters that are not a forward slash
            /            # "/"
            $            # End of string
        """,
        re.VERBOSE,
    )

    return bool(pattern.fullmatch(source_url))


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ("found_useful", AsanaUrlExistsFilter)
    list_display = ("id", "found_useful", "vote", "comments", "created")
    readonly_fields = [f.name for f in Feedback._meta.get_fields()] + ["preview_url"]
    ordering = ("-created", "id")
    actions = [send_to_asana]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            re_path("export_all/", self.export_all_feedback),
            re_path("export_comments/", self.export_feedback_with_comments),
        ]
        return my_urls + urls

    def preview_url(self, obj):
        if check_source_url_for_preview(
            obj.source_url
        ) and url_has_allowed_host_and_scheme(obj.source_url, allowed_hosts=None):
            link = self.request.build_absolute_uri(obj.source_url)
            return mark_safe('<a href="%s">%s</a>' % (link, link))
        return "-"

    def export_all_feedback(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied")
        return self.export(Feedback.objects.all().order_by("-created", "id"))

    def export_feedback_with_comments(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied")
        return self.export(
            Feedback.objects.all()
            .exclude(comments="")
            .order_by("found_useful", "vote", "-created", "id")
        )

    def export(self, qs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="feedback-%s.csv"' % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        )
        fields = ["id", "created", "comments", "found_useful", "vote", "source_url"]
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in qs:
            writer.writerow([getattr(row, field) for field in fields])
        return response


class NoElectionFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "no_election_feedback_text", "created")
    readonly_fields = [f.name for f in NoElectionFeedback._meta.get_fields()] + [
        "preview_url"
    ]
    ordering = ("-created", "id")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            re_path("export_all/", self.export_all_feedback),
        ]
        return my_urls + urls

    def preview_url(self, obj):
        if check_source_url_for_preview(
            obj.source_url
        ) and url_has_allowed_host_and_scheme(obj.source_url, allowed_hosts=None):
            link = self.request.build_absolute_uri(obj.source_url)
            return mark_safe('<a href="%s">%s</a>' % (link, link))
        return "-"

    def export_all_feedback(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access Denied")
        return self.export(NoElectionFeedback.objects.all().order_by("-created", "id"))

    def export(self, qs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="feedback-%s.csv"' % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        )
        fields = ["id", "created", "no_election_feedback_text", "source_url"]
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in qs:
            writer.writerow([getattr(row, field) for field in fields])
        return response


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(NoElectionFeedback, NoElectionFeedbackAdmin)
