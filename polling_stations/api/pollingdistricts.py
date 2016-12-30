from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingDistrict


class PollingDistrictDataSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = PollingDistrict
        fields = ('name', 'council')


class PollingDistrictGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PollingDistrict
        geo_field = 'area'
        fields = ('name', 'council')


class PollingDistrictViewSet(ReadOnlyModelViewSet):
    queryset = PollingDistrict.objects.all()
    serializer_class = PollingDistrictDataSerializer
