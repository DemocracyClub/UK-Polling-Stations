"""
Polling Stations Open Data API
"""

from django.utils.encoding import smart_str
from rest_framework import routers, serializers, viewsets
from councils.models import Council
from pollingstations.models import PollingStation, PollingDistrict

# Fields define serialization of complex field types (GEO)
class PointField(serializers.Field):    
    type_name = 'PointField'
    type_label = 'point'

    def to_representation(self, value):
        """
        Transform POINT object to json.
        """
        if value is None:
            return value

        value = {
            "latitude": smart_str(value.y),
            "longitude": smart_str(value.x)
        }
        return value


class PolygonField(serializers.Field):
    type_name = 'PolygonField'
    type_label = 'polygon'

    def to_representation(self, value):
        if value is None:
            return value
        return value.coords


# Serializers define the API representation.
class CouncilSerializer(serializers.HyperlinkedModelSerializer):
    location = PointField()
#    area = PolygonField()
    class Meta:
        model = Council
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
            'location', 
#            'area' # This is super slow ATM - TODO!
        )


class PollingStationSerializer(serializers.HyperlinkedModelSerializer):
    location = PointField()
    class Meta:
        model = PollingStation
        fields = ('council', 'postcode', 'address', 'location')


class PollingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    # area = PolygonField()
    class Meta: 
        model = PollingDistrict
        fields = (
            'name', 'council', 
#            'area' This is super slow ATM TODO!
        )


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
