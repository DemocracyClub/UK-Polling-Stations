from rest_framework.mixins import ListModelMixin
from rest_framework.reverse import reverse
from rest_framework.serializers import (
    CharField,
    HyperlinkedModelSerializer,
    SerializerMethodField,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)
from django.conf import settings
from django.utils.http import urlencode
from pollingstations.models import PollingStation
from .mixins import PollingEntityMixin


class PollingStationSerializer:
    def generate_urls(self, record):
        query_args = urlencode(
            {"council_id": record.council_id, "station_id": record.internal_council_id}
        )

        detail_url = u"%s?%s" % (
            reverse("pollingstation-list", request=self.context["request"]),
            query_args,
        )

        geo_url = u"%s?%s" % (
            reverse("pollingstation-geo", request=self.context["request"]),
            query_args,
        )

        return {"detail": detail_url, "geo": geo_url}


class PollingStationDataSerializer(
    PollingStationSerializer, HyperlinkedModelSerializer
):

    station_id = CharField(source="internal_council_id", read_only=True)
    urls = SerializerMethodField("generate_urls")

    class Meta:
        model = PollingStation
        fields = ("urls", "council", "station_id", "postcode", "address")


class PollingStationGeoSerializer(PollingStationSerializer, GeoFeatureModelSerializer):

    station_id = CharField(source="internal_council_id", read_only=True)
    id = SerializerMethodField("generate_id")
    urls = SerializerMethodField("generate_urls")
    council = SerializerMethodField("generate_council")
    location = GeometrySerializerMethodField("generate_location")

    def generate_council(self, record):
        return reverse(
            "council-detail",
            request=self.context["request"],
            kwargs={"pk": record.council_id},
        )

    def generate_id(self, record):
        return "%s.%s" % (record.council_id, record.internal_council_id)

    def generate_location(self, record):
        SHOW_MAPS = getattr(settings, "SHOW_MAPS", True)
        if not SHOW_MAPS:
            return None
        return record.location

    class Meta:
        model = PollingStation
        geo_field = "location"
        id_field = "id"
        fields = (
            "id",
            "urls",
            "council",
            "station_id",
            "postcode",
            "address",
            "location",
        )


class PollingStationViewSet(PollingEntityMixin, GenericViewSet, ListModelMixin):
    queryset = PollingStation.objects.all()
    id_field = "station_id"

    def get_queryset(self):
        council_id = self.request.query_params.get("council_id", None)
        station_id = self.request.query_params.get(self.id_field, None)

        if council_id is None:
            return PollingStation.objects.all()

        if station_id is None:
            return PollingStation.objects.filter(council=council_id)

        return PollingStation.objects.filter(
            council=council_id, internal_council_id=station_id
        )

    def get_serializer_class(self):
        if self.geo:
            return PollingStationGeoSerializer
        return PollingStationDataSerializer
