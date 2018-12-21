from django.http import HttpResponse
from django.views.generic import View, UpdateView
from django.utils.http import is_safe_url
from django.contrib import messages

from .forms import FeedbackForm
from .models import Feedback


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
            is_safe_url(self.object.source_url)
            and self.object.source_url != "/feedback/"
        ):
            return self.object.source_url
        else:
            return "/"


class RecordJsonFeedback(View):
    def post(self, request):
        found_useful = request.POST.get("found_useful")
        source_url = request.POST.get("source_url")
        token = request.POST.get("token")
        Feedback.objects.update_or_create(
            token=token,
            defaults={"found_useful": found_useful, "source_url": source_url},
        )
        return HttpResponse()
