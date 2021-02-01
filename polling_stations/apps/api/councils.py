from django.http import HttpResponsePermanentRedirect, Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.exceptions import ObjectDoesNotExist
from councils.models import Council


def contact_type_to_dict(obj, contact_type):
    """
    Build the contact details for a contact type in to a dict
    """

    assert contact_type in ["electoral_services", "registration"]
    data = {}
    for key in ["phone_numbers", "email", "address", "postcode", "website"]:
        data[key] = getattr(obj, "{}_{}".format(contact_type, key))
    if not any(data.values()):
        data = None
    return data


COUNCIL_FIELDS = (
    "url",
    "council_id",
    "name",
    "email",
    "phone",
    "website",
    "postcode",
    "address",
    "electoral_services_contacts",
    "registration_contacts",
    "identifiers",
    "nation",
)


class CouncilContactsMixin(object):
    def get_phone(self, obj):
        try:
            return obj.electoral_services_phone_numbers[0]
        except IndexError:
            return ""

    def get_electoral_services_contacts(self, obj):
        return contact_type_to_dict(obj, "electoral_services")

    def get_registration_contacts(self, obj):
        return contact_type_to_dict(obj, "registration")


class CouncilDataSerializer(
    serializers.HyperlinkedModelSerializer, CouncilContactsMixin
):
    class Meta:
        model = Council
        lookup_field = "council_id"
        fields = COUNCIL_FIELDS

    email = serializers.EmailField(source="electoral_services_email")
    phone = serializers.SerializerMethodField()
    website = serializers.URLField(source="electoral_services_website")
    postcode = serializers.CharField(source="electoral_services_postcode")
    address = serializers.CharField(source="electoral_services_address")

    electoral_services_contacts = serializers.SerializerMethodField()
    registration_contacts = serializers.SerializerMethodField()
    nation = serializers.CharField()


class CouncilGeoSerializer(GeoFeatureModelSerializer, CouncilContactsMixin):
    geography_model_geo_field = GeometrySerializerMethodField()

    def get_geography_model_geo_field(self, obj):
        return obj.geography.geography

    class Meta:
        model = Council
        geo_field = "geography_model_geo_field"
        id_field = "council_id"
        extra_kwargs = {"url": {"view_name": "council-geo", "lookup_field": "pk"}}
        fields = COUNCIL_FIELDS

    email = serializers.EmailField(source="electoral_services_email")
    phone = serializers.SerializerMethodField()
    website = serializers.URLField(source="electoral_services_website")
    postcode = serializers.CharField(source="electoral_services_postcode")
    address = serializers.CharField(source="electoral_services_address")

    electoral_services_contacts = serializers.SerializerMethodField()
    registration_contacts = serializers.SerializerMethodField()


class CouncilViewSet(ReadOnlyModelViewSet):
    queryset = Council.objects.all()
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
