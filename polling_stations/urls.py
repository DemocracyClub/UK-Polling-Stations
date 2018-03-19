# -*- coding: utf-8 -*-


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from apiblueprint_view.views import ApiBlueprintView

from api.router import router
from data_finder.views import (
    HomeView,
    PrivacyView,
    PostcodeView,
    ExamplePostcodeView,
    CoverageView,
    AddressView,
    AddressFormView,
    WeDontKnowView,
    MultipleCouncilsView,
)


core_patterns = [
    url(r'^postcode/(?P<postcode>.+)/$',
        PostcodeView.as_view(), name='postcode_view'),
    url(r'^postcode/$',
        PostcodeView.as_view(), name='postcode_view_alias'),
    url(r'^address/(?P<address_slug>.+)/$',
        AddressView.as_view(), name='address_view'),
    url(r'^we_dont_know/(?P<postcode>.+)/$',
        WeDontKnowView.as_view(), name='we_dont_know'),
    url(r'^multiple_councils/(?P<postcode>.+)/$',
        MultipleCouncilsView.as_view(), name='multiple_councils_view'),
    url(r'^address_select/(?P<postcode>.+)/$',
        AddressFormView.as_view(), name='address_select_view'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^privacy/$', PrivacyView.as_view(), name='privacy_view'),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
]

extra_patterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/beta/', include(router.urls)),
    url(r'^api/$', ApiBlueprintView.as_view(
        blueprint='polling_stations/templates/api_docs/blueprints/wheredoivote.apibp',
        template_name='api_docs/api_base_template.html',
        styles={
            'resource': {'class': 'card'},
            'resource_group': {'class': 'card'},
            'method_GET': {'class': 'badge success'},
        }), name='api_docs'
    ),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^league_table/', include('data_collection.urls')),
    url(r'^coverage/$', CoverageView.as_view(), name='coverage'),
    url(r'^example/$', ExamplePostcodeView.as_view(), name='example'),
    url(r'^email/', include('dc_signup_form.urls', namespace='dc_signup_form')),

    url(r'^about/$',
        RedirectView.as_view(
            url='https://democracyclub.org.uk/projects/polling-stations/',
            permanent=True
        ), name='about'),
]

PREFIXED_URLS = settings.EMBED_PREFIXES + settings.WHITELABEL_PREFIXES
for EMBED in PREFIXED_URLS:
    extra_patterns += [
        url(r'^%s/' % EMBED, include('whitelabel.urls')),
    ]

urlpatterns = extra_patterns + core_patterns + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler500 = 'dc_theme.urls.dc_server_error'
