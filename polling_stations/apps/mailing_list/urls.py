from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt


from dc_signup_form.forms import MailingListSignupForm
from dc_signup_form.views import SignupFormView

app_name = "mailing_list"

urlpatterns = [
    url(
        r"^signup/$",
        csrf_exempt(
            SignupFormView.as_view(
                template_name="base.html",
                form_class=MailingListSignupForm,
                backend="local_db",
            )
        ),
        name="mailing_list_signup_view",
    ),
    url(r"^api_signup/v1/", include("dc_signup_form.signup_server.urls")),
]
