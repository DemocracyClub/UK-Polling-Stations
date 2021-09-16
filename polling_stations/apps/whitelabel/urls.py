from django.urls import include, re_path
from polling_stations.urls import core_patterns

urlpatterns = [re_path(r"", include(core_patterns))]
