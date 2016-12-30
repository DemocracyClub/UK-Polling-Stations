from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from councils.models import Council


class CouncilDataSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Council
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
        )


class CouncilGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Council
        geo_field = 'area'
        id_field = 'council_id'
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
        )


class CouncilViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']
    queryset = Council.objects.all()
    serializer_class = CouncilDataSerializer
