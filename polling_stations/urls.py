# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from data_finder.views import HomeView, CouncilView, PostcodeView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework import routers, serializers, viewsets
from councils.models import Council
from pollingstations.models import PollingStation, PollingDistrict

# Serializers define the API representation.
class CouncilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Council
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address'
        )


class PollingStationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PollingStation
        fields = ('council', 'postcode', 'address', 'location')


class PollingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = PollingDistrict
        fields = ('name', 'council', 'area')


# ViewSets define the view behavior.
class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = CouncilSerializer


class PollingStationViewSet(viewsets.ModelViewSet):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer


class PollingDistrictViewSet(viewsets.ModelViewSet):
    queryset = PollingDistrict.objects.all()
    serializer_class = PollingDistrictSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'councils', CouncilViewSet)
router.register(r'pollingstations', PollingStationViewSet)
router.register(r'pollingdistricts', PollingDistrictViewSet)
        



urlpatterns = patterns(
    '',
    url(r'api/', include(router.urls)),
  
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^league_table/', include('data_collection.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^council/(?P<pk>.+)/$', CouncilView.as_view(), name='council'),
    url(r'^postcode/(?P<postcode>.+)/$',
        PostcodeView.as_view(), name='postcode_view'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

