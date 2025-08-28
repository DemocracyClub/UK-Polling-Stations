from django.contrib import messages
from django.http import HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import UpdateView, View

from .forms import FeedbackForm, NoElectionFeedbackForm
from .models import Feedback, NoElectionFeedback


class FeedbackFormView(UpdateView):
    form_class = FeedbackForm
    template_name = "feedback/feedback_form_view.html"

    def get_object(self, queryset=None):
        token = self.request.POST.get("token")
        try:
            return Feedback.objects.get(token=token)
        except Feedback.DoesNotExist:
            return Feedback(token=token)

    def get_success_url(self):
        messages.success(self.request, "Thank you for your feedback!")

        if (
            url_has_allowed_host_and_scheme(self.object.source_url, allowed_hosts=None)
            and self.object.source_url != "/feedback/"
        ):
            return self.object.source_url
        return "/"


class NoElectionFeedbackFormView(FeedbackFormView):
    form_class = NoElectionFeedbackForm
    template_name = "feedback/no_election_feedback_form_view.html"

    def get_object(self, queryset=None):
        token = self.request.POST.get("token")
        try:
            return NoElectionFeedback.objects.get(token=token)
        except NoElectionFeedback.DoesNotExist:
            return NoElectionFeedback(token=token)


class RecordJsonFeedback(View):
    def post(self, request):
        fields = {
            "found_useful": request.POST.get("found_useful", ""),
            "vote": request.POST.get("vote", ""),
        }
        token = request.POST.get("token")

        try:
            feedback = Feedback.objects.get(token=token)
        except Feedback.DoesNotExist:
            feedback = Feedback(token=token)
            feedback.source_url = request.POST.get("source_url")

        for key, value in fields.items():
            if key in request.POST:
                setattr(feedback, key, value)

        feedback.save()

        return HttpResponse()
