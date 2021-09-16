from django.urls import re_path

from .views import BugReportFormView

urlpatterns = [re_path(r"^$", BugReportFormView.as_view(), name="bug_report_form_view")]
