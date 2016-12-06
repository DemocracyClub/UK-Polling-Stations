from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from .views import LeagueTable, MorphReport

urlpatterns = patterns(
    '',
    url(r'^/$', LeagueTable.as_view(), name='league_table'),
    url(r'/scraper_report/$', MorphReport.as_view(), name='scraper_report'),
    url(r'/data_quality/(?P<council_id>.+)/$', 'data_collection.views.data_quality', name='data_quality'),
)

