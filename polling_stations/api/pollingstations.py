from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingStation


class PollingStationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PollingStation
        geo_field = 'location'
        fields = ('council', 'postcode', 'address', 'location')


class PollingStationViewSet(GenericViewSet, ListModelMixin):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer
