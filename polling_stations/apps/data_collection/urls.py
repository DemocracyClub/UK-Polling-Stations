from django.conf.urls import url
from django.views.generic import RedirectView


urlpatterns = [
    url(r"^$", RedirectView.as_view(pattern_name="home"), name="league_table"),
    url(
        r"data_quality/(?P<pk>.+)/$",
        RedirectView.as_view(pattern_name="dashboard:council_detail"),
        name="data_quality",
    ),
]
