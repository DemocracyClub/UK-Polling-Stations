from django.conf.urls import url

from . import views

app_name = "dashboard"

urlpatterns = [
    url(r"^$", views.IndexView.as_view(), name="index"),
    url(
        r"council/(?P<pk>[^/]+)/$",
        views.CouncilDetailView.as_view(),
        name="council_detail",
    ),
    url(
        r"council/(?P<council_pk>[^/]+)/polling-station/(?P<id>.+)/$",
        views.PollingStationDetailView.as_view(),
        name="pollingstation_detail",
    ),
    url(
        r"postcode/(?P<postcode>[^/]+)/$", views.PostCodeView.as_view(), name="postcode"
    ),
    url(
        r"postcode/(?P<postcode>[^/]+).geojson$",
        views.PostCodeGeoJSONView.as_view(),
        name="postcode-geojson",
    ),
]
