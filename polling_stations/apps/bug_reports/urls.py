from django.conf.urls import url

from .views import BugReportFormView

urlpatterns = [
    url(r'^$', BugReportFormView.as_view(), name='bug_report_form_view'),
]
