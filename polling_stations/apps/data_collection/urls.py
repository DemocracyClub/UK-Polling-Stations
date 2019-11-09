from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r"^$", RedirectView.as_view(url=reverse_lazy("home")), name="league_table"),
    url(
        r"data_quality/(?P<council_id>.+)/$",
        RedirectView.as_view(url=reverse_lazy("home")),
        name="data_quality",
    ),
]
