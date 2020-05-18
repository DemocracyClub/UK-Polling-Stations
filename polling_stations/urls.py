# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from dc_theme.urls import dc_server_error

from api.router import router
from api.docs import ApiDocsView
from data_finder.views import (
    HomeView,
    PostcodeView,
    ExamplePostcodeView,
    AddressView,
    AddressFormView,
    WeDontKnowView,
)
from pollingstations.views import status_check


admin.autodiscover()


core_patterns = [
    url(r"^status_check/$", status_check, name="status_check"),
    url(r"^postcode/(?P<postcode>.+)/$", PostcodeView.as_view(), name="postcode_view"),
    url(r"^postcode/$", PostcodeView.as_view(), name="postcode_view_alias"),
    url(r"^address/(?P<uprn>.+)/$", AddressView.as_view(), name="address_view"),
    url(
        r"^we_dont_know/(?P<postcode>.+)/$",
        WeDontKnowView.as_view(),
        name="we_dont_know",
    ),
    url(
        r"^address_select/(?P<postcode>.+)/$",
        AddressFormView.as_view(),
        name="address_select_view",
    ),
    url(r"^$", HomeView.as_view(), name="home"),
    url(
        r"^privacy/$",
        RedirectView.as_view(
            url="https://democracyclub.org.uk/privacy/", permanent=True
        ),
        name="privacy_view",
    ),
    url(
        r"^robots\.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

extra_patterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^i18n/", include("django.conf.urls.i18n")),
    url(r"^api/beta/", include(router.urls)),
    url(r"^api/$", ApiDocsView.as_view(), name="api_docs"),
    url(r"^admin/", admin.site.urls),
    url(r"^feedback/", include("feedback.urls")),
    url(r"^report_problem/", include("bug_reports.urls")),
    url(r"^uploads/", include("file_uploads.urls", namespace="file_uploads")),
    url(r"^example/$", ExamplePostcodeView.as_view(), name="example"),
    url(r"^email/", include("dc_signup_form.urls", namespace="dc_signup_form")),
    url(
        r"^about/$",
        RedirectView.as_view(
            url="https://democracyclub.org.uk/projects/polling-stations/",
            permanent=True,
        ),
        name="about",
    ),
]

if "dashboard" in settings.INSTALLED_APPS:
    extra_patterns.append(
        url(r"^dashboard/", include("dashboard.urls", namespace="dashboard"))
    )

PREFIXED_URLS = settings.EMBED_PREFIXES + settings.WHITELABEL_PREFIXES
for EMBED in PREFIXED_URLS:
    extra_patterns += [url(r"^%s/" % EMBED, include("whitelabel.urls"))]

urlpatterns = (
    extra_patterns
    + core_patterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

handler500 = dc_server_error
