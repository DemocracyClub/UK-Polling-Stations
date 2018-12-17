from .forms import FeedbackForm


def feedback_form(request):
    return {"feedback_form": FeedbackForm(initial={"source_url": request.path})}
