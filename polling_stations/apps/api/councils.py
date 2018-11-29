from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from councils.models import Council


class CouncilDataSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Council
        lookup_field = 'council_id'
        fields = (
            'url', 'council_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
        )


class CouncilGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Council
        geo_field = 'area'
        id_field = 'council_id'
        extra_kwargs = {
            'url': {'view_name': 'council-geo', 'lookup_field': 'pk'}
        }
        fields = (
            'url', 'council_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
        )


class CouncilViewSet(ReadOnlyModelViewSet):
    queryset = Council.objects.all().defer("area")
    serializer_class = CouncilDataSerializer

    @detail_route(url_path='geo')
    def geo(self, request, pk=None, format=None):
        try:
            council = Council.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Not found.'}, 404)
        except:
            return Response({'detail': 'Internal server error'}, 500)

        return Response(
            CouncilGeoSerializer(council, context={'request': request}).data)
