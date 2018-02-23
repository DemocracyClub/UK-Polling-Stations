from django.conf.urls import url

from .views import FeedbackFormView, RecordJsonFeedback

urlpatterns = [
    url(
        r'^submit_initial/',
        RecordJsonFeedback.as_view(),
        name='json_feedback_view'),
    url(
        r'^$',
        FeedbackFormView.as_view(),
        name='feedback_form_view'),
]
