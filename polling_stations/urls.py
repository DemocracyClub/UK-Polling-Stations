# -*- coding: utf-8 -*-
from api.router import router
import data_finder.views as data_finder_views
from data_finder import review_views
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from pollingstations.views import status_check

admin.autodiscover()

core_patterns = [
    re_path(r"^status_check/$", status_check, name="status_check"),
    re_path(
        r"^postcode/(?P<postcode>.+)/$",
        data_finder_views.PostcodeView.as_view(),
        name="postcode_view",
    ),
    re_path(
        r"^postcode/$",
        data_finder_views.PostcodeView.as_view(),
        name="postcode_view_alias",
    ),
    re_path(
        r"^address/(?P<uprn>.+)/$",
        data_finder_views.AddressView.as_view(),
        name="address_view",
    ),
    re_path(
        r"^we_dont_know/(?P<postcode>.+)/$",
        data_finder_views.WeDontKnowView.as_view(),
        name="we_dont_know",
    ),
    re_path(
        r"^multiple_councils/(?P<postcode>.+)/$",
        data_finder_views.MultipleCouncilsView.as_view(),
        name="multiple_councils_view",
    ),
    re_path(
        r"^address_select/(?P<postcode>.+)/$",
        data_finder_views.AddressFormView.as_view(),
        name="address_select_view",
    ),
    re_path(r"^$", data_finder_views.HomeView.as_view(), name="home"),
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
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^feedback/", include("feedback.urls")),
    re_path(r"^report_problem/", include("bug_reports.urls")),
    re_path(r"^uploads/", include("file_uploads.urls", namespace="file_uploads")),
    re_path(
        r"^example/$", data_finder_views.ExamplePostcodeView.as_view(), name="example"
    ),
    re_path(
        r"^about/$",
        RedirectView.as_view(
            url="https://democracyclub.org.uk/projects/polling-stations/",
            permanent=True,
        ),
        name="about",
    ),
]

boundary_review_patterns = (
    [
        re_path(
            r"^WLL/20250609/postcode/(?P<postcode>.+)/$",
            review_views.PostcodeView.as_view(),
            name="postcode_view",
        ),
        re_path(
            r"^WLL/20250609/postcode/$",
            review_views.PostcodeView.as_view(),
            name="postcode_view_alias",
        ),
        re_path(
            r"^WLL/20250609/address/(?P<uprn>.+)/$",
            review_views.AddressView.as_view(),
            name="address_view",
        ),
        re_path(
            r"^WLL/20250609/we_dont_know/(?P<postcode>.+)/$",
            review_views.WeDontKnowView.as_view(),
            name="we_dont_know",
        ),
        re_path(
            r"^WLL/20250609/address_select/(?P<postcode>.+)/$",
            review_views.AddressFormView.as_view(),
            name="address_select_view",
        ),
        re_path(r"^WLL/20250609/$", review_views.HomeView.as_view(), name="home"),
    ],
    "reviews",
)

if "dashboard" in settings.INSTALLED_APPS:
    extra_patterns.append(
        re_path(r"^dashboard/", include("dashboard.urls", namespace="dashboard"))
    )

if getattr(settings, "ENABLE_API_DOCS", False):
    extra_patterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
        path(
            "api/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger",
        ),
    ]

if "debug_toolbar" in settings.INSTALLED_APPS:
    extra_patterns.append(
        path("__debug__/", include("debug_toolbar.urls")),
    )

PREFIXED_URLS = settings.EMBED_PREFIXES + settings.WHITELABEL_PREFIXES
for EMBED in PREFIXED_URLS:
    extra_patterns += [re_path(r"^%s/" % EMBED, include("whitelabel.urls"))]

urlpatterns = (
    extra_patterns
    + core_patterns
    + [path("reviews/", include(boundary_review_patterns))]
)

handler500 = "dc_utils.urls.dc_server_error"

if settings.DEBUG:
    from dc_utils.urls import dc_utils_testing_patterns

    urlpatterns += dc_utils_testing_patterns
