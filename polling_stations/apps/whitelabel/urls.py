from django.conf.urls import patterns, include, url
from django.conf import settings

from polling_stations.urls import core_patterns

urlpatterns = patterns(
    '',
    url(r'', include(core_patterns)),
)

