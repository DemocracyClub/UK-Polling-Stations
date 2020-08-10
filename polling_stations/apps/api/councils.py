from django.http import HttpResponsePermanentRedirect, Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.reverse import reverse
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

    def retrieve(self, request, *args, **kwargs):
        """
        A Council can have more than one ID, as defined across the pk and the
        list of `identifiers` on the model. If a non-PK identifier is used as
        the PK argument in the URL, look up the instance and redirect to the
        canonical URL for this instance.

        This is useful for example when a GSS code is used to request a council
        when the canonical ID is the council register code.
        """
        try:
            self.get_object()
        except Http404:
            try:
                queryset = self.filter_queryset(self.get_queryset())
                obj = queryset.get(identifiers__contains=[self.kwargs["pk"]])
                return HttpResponsePermanentRedirect(
                    reverse(
                        "council-detail", kwargs={"pk": obj.pk}, request=self.request
                    )
                )
            except Council.DoesNotExist:
                # Let the super() catch this and raise a Http404
                pass
        return super().retrieve(request, *args, **kwargs)

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
