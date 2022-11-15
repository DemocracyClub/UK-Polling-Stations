# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from api.router import router
from api.docs import ApiDocsView
from data_finder.views import (
    HomeView,
    PostcodeView,
    ExamplePostcodeView,
    AddressView,
    AddressFormView,
    WeDontKnowView,
    MultipleCouncilsView,
)
from pollingstations.views import status_check


admin.autodiscover()


core_patterns = [
    re_path(r"^status_check/$", status_check, name="status_check"),
    re_path(
        r"^postcode/(?P<postcode>.+)/$", PostcodeView.as_view(), name="postcode_view"
    ),
    re_path(r"^postcode/$", PostcodeView.as_view(), name="postcode_view_alias"),
    re_path(r"^address/(?P<uprn>.+)/$", AddressView.as_view(), name="address_view"),
    re_path(
        r"^we_dont_know/(?P<postcode>.+)/$",
        WeDontKnowView.as_view(),
        name="we_dont_know",
    ),
    re_path(
        r"^multiple_councils/(?P<postcode>.+)/$",
        MultipleCouncilsView.as_view(),
        name="multiple_councils_view",
    ),
    re_path(
        r"^address_select/(?P<postcode>.+)/$",
        AddressFormView.as_view(),
        name="address_select_view",
    ),
    re_path(r"^$", HomeView.as_view(), name="home"),
    re_path(
        r"^privacy/$",
        RedirectView.as_view(
            url="https://democracyclub.org.uk/privacy/", permanent=True
        ),
        name="privacy_view",
    ),
    re_path(
        r"^robots\.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("i18n/", include("django.conf.urls.i18n")),
]

extra_patterns = [
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    re_path(r"^api/beta/", include(router.urls)),
    re_path(r"^api/$", ApiDocsView.as_view(), name="api_docs"),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^feedback/", include("feedback.urls")),
    re_path(r"^report_problem/", include("bug_reports.urls")),
    re_path(r"^uploads/", include("file_uploads.urls", namespace="file_uploads")),
    re_path(r"^example/$", ExamplePostcodeView.as_view(), name="example"),
    re_path(
        r"^about/$",
        RedirectView.as_view(
            url="https://democracyclub.org.uk/projects/polling-stations/",
            permanent=True,
        ),
        name="about",
    ),
    re_path(r"^email/", include("dc_signup_form.urls")),
]

if "dashboard" in settings.INSTALLED_APPS:
    extra_patterns.append(
        re_path(r"^dashboard/", include("dashboard.urls", namespace="dashboard"))
    )

PREFIXED_URLS = settings.EMBED_PREFIXES + settings.WHITELABEL_PREFIXES
for EMBED in PREFIXED_URLS:
    extra_patterns += [re_path(r"^%s/" % EMBED, include("whitelabel.urls"))]

urlpatterns = extra_patterns + core_patterns

handler500 = "dc_utils.urls.dc_server_error"

if settings.DEBUG:
    from dc_utils.urls import dc_utils_testing_patterns

    urlpatterns += dc_utils_testing_patterns
