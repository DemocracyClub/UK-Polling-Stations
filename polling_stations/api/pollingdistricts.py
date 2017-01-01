from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import (
    CharField,
    HyperlinkedModelSerializer,
    SerializerMethodField
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingDistrict
from .mixins import PollingEntityMixin


class PollingDistrictDataSerializer(HyperlinkedModelSerializer):

    district_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingDistrict
        fields = ('council', 'district_id', 'name')


class PollingDistrictGeoSerializer(GeoFeatureModelSerializer):

    district_id = CharField(source='internal_council_id', read_only=True)
    id = SerializerMethodField('generate_id')

    def generate_id(self, record):
        return "%s.%s" % (record.council_id, record.internal_council_id)

    class Meta:
        model = PollingDistrict
        geo_field = 'area'
        id_field = 'id'
        fields = ('id', 'council', 'district_id', 'name')


class PollingDistrictViewSet(PollingEntityMixin, GenericViewSet, ListModelMixin):
    queryset = PollingDistrict.objects.all()

    def get_queryset(self):
        council_id = self.request.query_params.get('council_id', None)
        district_id = self.request.query_params.get('district_id', None)

        if council_id is None:
            return PollingDistrict.objects.all()

        if district_id is None:
            return PollingDistrict.objects.filter(council=council_id)

        return PollingDistrict.objects.filter(
            council=council_id, internal_council_id=district_id)

    def get_serializer_class(self):
        if self.geo:
            return PollingDistrictGeoSerializer
        return PollingDistrictDataSerializer

    def validate_request(self):
        if 'district_id' in self.request.query_params and\
                'council_id' not in self.request.query_params:
            return False
        return True
