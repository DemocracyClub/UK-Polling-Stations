import csv
import datetime
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ("found_useful",)
    list_display = ("id", "found_useful", "comments", "created")
    readonly_fields = [f.name for f in Feedback._meta.get_fields()]
    ordering = ("-created", "id")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url("export_all/", self.export_all_feedback),
            url("export_comments/", self.export_feedback_with_comments),
        ]
        return my_urls + urls

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
            .order_by("found_useful", "-created", "id")
        )

    def export(self, qs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="feedback-%s.csv"' % (
            datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        )
        fields = ["id", "created", "comments", "found_useful", "source_url"]
        writer = csv.writer(response)
        writer.writerow(fields)
        for row in qs:
            writer.writerow([getattr(row, field) for field in fields])
        return response


admin.site.register(Feedback, FeedbackAdmin)
