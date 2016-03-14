# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from polling_stations.api import router
from data_finder.views import (
    HomeView,
    CouncilView,
    PostcodeView,
    CoverageView,
    AddressView,
    AddressFormView
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



core_patterns = patterns(
    url(r'^council/(?P<pk>.+)/$', CouncilView.as_view(), name='council'),
    url(r'^postcode/(?P<postcode>.+)/$',
        PostcodeView.as_view(), name='postcode_view'),
    url(r'^address/(?P<address_id>.+)/$',
        AddressView.as_view(), name='address_view'),
    url(r'^address_select/(?P<postcode>.+)/$',
        AddressFormView.as_view(), name='address_select_view'),
    url(r'^$', HomeView.as_view(), name='home'),
)

extra_patterns = patterns(
    '',

    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^league_table', include('data_collection.urls')),
    url(r'^coverage$', CoverageView.as_view(), name='coverage'),

    url(r'^about$', TemplateView.as_view(template_name='about.html'), name='about'),
)

for EMBED in settings.EMBED_PREFIXES:
    extra_patterns += patterns(
        '',
        url(r'^%s/' % EMBED, include('whitelabel.urls')),
    )

urlpatterns =  extra_patterns + core_patterns + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

