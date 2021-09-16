from django.urls import re_path

from .views import FeedbackFormView, RecordJsonFeedback

urlpatterns = [
    re_path(
        r"^submit_initial/", RecordJsonFeedback.as_view(), name="json_feedback_view"
    ),
    re_path(r"^$", FeedbackFormView.as_view(), name="feedback_form_view"),
]
