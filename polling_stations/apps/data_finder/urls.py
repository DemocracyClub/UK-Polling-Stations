from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from constituencies.views import ConstituencyList, ConstituencyView

urlpatterns = patterns(
    '',
    url(r'^/$',  cache_page(60*60)(ConstituencyList.as_view()), name='constituencies'),
    # url(r'^/notspots/', view_not_spots, name='constituency_notspots'),
    url(r'^/(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$',
            ConstituencyView.as_view(),
            name='constituency-view'),
)

