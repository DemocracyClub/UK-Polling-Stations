from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from councils.models import Council


class CouncilDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Council
        lookup_field = "council_id"
        fields = (
            "url",
            "council_id",
            "name",
            "email",
            "phone",
            "website",
            "postcode",
            "address",
        )

    email = serializers.EmailField(source="electoral_services_email")
    phone = serializers.SerializerMethodField()
    website = serializers.URLField(source="electoral_services_website")
    postcode = serializers.CharField(source="electoral_services_postcode")
    address = serializers.CharField(source="electoral_services_address")

    def get_phone(self, obj):
        return obj.electoral_services_phone_numbers[0]


class CouncilGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Council
        geo_field = "area"
        id_field = "council_id"
        extra_kwargs = {"url": {"view_name": "council-geo", "lookup_field": "pk"}}
        fields = (
            "url",
            "council_id",
            "name",
            "email",
            "phone",
            "website",
            "postcode",
            "address",
        )

    email = serializers.EmailField(source="electoral_services_email")
    phone = serializers.SerializerMethodField()
    website = serializers.URLField(source="electoral_services_website")
    postcode = serializers.CharField(source="electoral_services_postcode")
    address = serializers.CharField(source="electoral_services_address")

    def get_phone(self, obj):
        return obj.electoral_services_phone_numbers[0]


class CouncilViewSet(ReadOnlyModelViewSet):
    queryset = Council.objects.all().defer("area")
    serializer_class = CouncilDataSerializer

    @action(detail=True, url_path="geo")
    def geo(self, request, pk=None, format=None):
        try:
            council = Council.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, 404)
        except:
            return Response({"detail": "Internal server error"}, 500)

        return Response(
            CouncilGeoSerializer(council, context={"request": request}).data
        )
