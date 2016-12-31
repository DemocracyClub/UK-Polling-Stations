from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.serializers import CharField, HyperlinkedModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingDistrict


class PollingDistrictDataSerializer(HyperlinkedModelSerializer):

    district_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingDistrict
        fields = ('council', 'district_id', 'name')


class PollingDistrictGeoSerializer(GeoFeatureModelSerializer):

    district_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingDistrict
        geo_field = 'area'
        fields = ('council', 'district_id', 'name')


class PollingDistrictViewSet(GenericViewSet, ListModelMixin):
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

    def validate_request(self):
        if 'district_id' in self.request.query_params and\
            'council_id' not in self.request.query_params:
                return False
        return True

    def list(self, request, *args, **kwargs):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()
        serializer = PollingDistrictDataSerializer(
            queryset, many=True, read_only=True, context={'request': request})
        return Response(serializer.data)

    @list_route(url_path='geo')
    def geo(self, request, format=None):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()
        serializer = PollingDistrictGeoSerializer(
            queryset, many=True, read_only=True, context={'request': request})
        return Response(serializer.data)
