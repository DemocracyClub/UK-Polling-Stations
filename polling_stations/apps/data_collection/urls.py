from django.conf.urls import include, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from .views import LeagueTable, data_quality

urlpatterns = [
    url(r'^/$', LeagueTable.as_view(), name='league_table'),
    url(r'/data_quality/(?P<council_id>.+)/$', data_quality, name='data_quality'),
]
