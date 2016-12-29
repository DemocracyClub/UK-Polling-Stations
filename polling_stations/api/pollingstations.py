from rest_framework import serializers, viewsets
from pollingstations.models import PollingStation
from .fields import PointField


class PollingStationSerializer(serializers.HyperlinkedModelSerializer):
    location = PointField()

    class Meta:
        model = PollingStation
        fields = ('council', 'postcode', 'address', 'location')


class PollingStationViewSet(viewsets.ModelViewSet):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer
