from django.urls import re_path

from . import views

app_name = "dashboard"

urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="index"),
    re_path(
        r"council/(?P<pk>[^/]+)/$",
        views.CouncilDetailView.as_view(),
        name="council_detail",
    ),
    re_path(
        r"council/(?P<council_pk>[^/]+)/polling-station/(?P<id>.+)/$",
        views.PollingStationDetailView.as_view(),
        name="pollingstation_detail",
    ),
    re_path(
        r"postcode/(?P<postcode>[^/]+)/$", views.PostCodeView.as_view(), name="postcode"
    ),
    re_path(
        r"postcode/(?P<postcode>[^/]+).geojson$",
        views.PostCodeGeoJSONView.as_view(),
        name="postcode-geojson",
    ),
]
