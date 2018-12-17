from django.conf.urls import include, url
from polling_stations.urls import core_patterns

urlpatterns = [url(r"", include(core_patterns))]
