from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView
from .forms import BugReportForm
from django.contrib import messages


class BugReportFormView(CreateView):
    form_class = BugReportForm
    template_name = 'bug_reports/report_form_view.html'

    def get_success_url(self):
        messages.success(self.request, 'Thank you for your feedback!')

        if self.source_redirect and\
            is_safe_url(self.object.source_url) and\
            'report_problem' not in self.object.source_url:

            return self.object.source_url
        else:
            return "/"

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            report = form.save()

            report.status = 'OPEN'
            report.report_type = 'OTHER'
            report.user_agent = request.META.get('HTTP_USER_AGENT', '')

            # if the source_url came from our hidden field
            # we'll try to redirect to it if it passes 'is_safe_url()'
            self.source_redirect = True

            # try to populate these from request params
            # if they weren't submitted with the form
            if not report.source_url:
                report.source_url = request.GET.get('source_url', '')

                # if the source_url came from request.GET
                # we don't want to try and redirect
                # even if it passes 'is_safe_url()'
                self.source_redirect = False

            if not report.source:
                report.source = request.GET.get('source', '')

            report.save()
            self.object = report
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)
