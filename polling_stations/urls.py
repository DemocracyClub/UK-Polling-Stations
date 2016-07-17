# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from polling_stations.api import router
from data_finder.views import (
    HomeView,
    PrivacyView,
    PostcodeView,
    CoverageView,
    AddressView,
    AddressFormView,
    campaign_signup
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


core_patterns = patterns(
    '',
    url(r'^postcode/(?P<postcode>.+)/$',
        PostcodeView.as_view(), name='postcode_view'),
    url(r'^address/(?P<address_slug>.+)/$',
        AddressView.as_view(), name='address_view'),
    url(r'^address_select/(?P<postcode>.+)/$',
        AddressFormView.as_view(), name='address_select_view'),
    url(r'^campaign_signup/(?P<postcode>.+)/$',
        'data_finder.views.campaign_signup', name='campaign_signup'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^privacy/$', PrivacyView.as_view(), name='privacy_view'),
)

extra_patterns = patterns(
    '',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^league_table', include('data_collection.urls')),
    url(r'^coverage$', CoverageView.as_view(), name='coverage'),

    url(r'^about$',
        RedirectView.as_view(
            url='https://democracyclub.org.uk/projects/polling-stations/',
            permanent=True
        ), name='about'),
)

PREFIXED_URLS = settings.EMBED_PREFIXES + settings.WHITELABEL_PREFIXES
for EMBED in PREFIXED_URLS:
    extra_patterns += patterns(
        '',
        url(r'^%s/' % EMBED, include('whitelabel.urls')),
    )

urlpatterns =  extra_patterns + core_patterns+ static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)

