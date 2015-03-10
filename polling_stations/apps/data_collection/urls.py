from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from .views import LeagueTable

urlpatterns = patterns(
    '',
    url(r'^$',  LeagueTable.as_view(), name='league_table'),
)

