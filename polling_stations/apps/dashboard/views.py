import json
import operator
from functools import reduce

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from councils.models import Council
from pollingstations.models import ResidentialAddress, PollingStation


class DashboardMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IndexView(DashboardMixin, ListView):
    queryset = Council.objects.select_related("dataquality")
    template_name = "dashboard/council_list.html"


class CouncilDetailView(DashboardMixin, DetailView):
    queryset = Council.objects.all()
    template_name = "dashboard/council_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(object=object, **kwargs)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT postcode, st_maxdistance(multipoint, multipoint)::int AS maxdistance
                FROM (
                    SELECT postcode, st_transform(st_collect(location), 27700) AS multipoint
                    FROM pollingstations_residentialaddress
                    WHERE council_id = %s
                    GROUP BY postcode
                ) AS subquery
                WHERE multipoint IS NOT NULL
                ORDER BY maxdistance DESC
                LIMIT 10;
            """,
                (object.pk,),
            )
            context["postcodes_by_diameter"] = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT ps.internal_council_id,
                   ra.address,
                   ra.slug,
                   ra.postcode,
                   st_distance(st_transform(ps.location, 27700), st_transform(ra.location, 27700))::int AS distance
                FROM pollingstations_pollingstation ps,
                     pollingstations_residentialaddress ra
                WHERE ps.council_id=ra.council_id
                  AND ra.polling_station_id=ps.internal_council_id
                  AND ra.council_id=%s
                  AND ra.location IS NOT NULL
                  AND ps.location IS NOT NULL
                ORDER BY distance DESC
                LIMIT 10;
            """,
                (object.pk,),
            )
            context["distances_to_stations"] = cursor.fetchall()

        context["pollingstation_list"] = PollingStation.objects.filter(council=object)

        return context


class PostCodeView(TemplateView):
    template_name = "dashboard/postcode.html"

    def get_context_data(self, postcode, **kwargs):
        return {
            "postcode": postcode,
            "addresses": ResidentialAddress.objects.filter(postcode=postcode),
        }


class PostCodeGeoJSONView(View):
    station_colors = ["purple", "red", "blue", "yellow", "green", "pink", "orange"]

    def get(self, request, postcode):
        residential_addresses = ResidentialAddress.objects.filter(postcode=postcode)
        station_ids = sorted(
            set(residential_addresses.values_list("council_id", "polling_station_id"))
        )
        stations = PollingStation.objects.filter(
            reduce(
                operator.or_,
                (
                    Q(council_id=council_id, internal_council_id=internal_council_id)
                    for council_id, internal_council_id in station_ids
                ),
            )
        )
        station_colors = dict(zip(station_ids, self.station_colors))

        return JsonResponse(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": json.loads(station.location.geojson)
                        if station.location
                        else None,
                        "properties": {
                            "type": "pollingstation",
                            "council_id": station.council_id,
                            "internal_council_id": station.internal_council_id,
                            "address": station.address,
                            "color": station_colors[
                                (station.council_id, station.internal_council_id)
                            ],
                            "url": reverse(
                                "dashboard:pollingstation_detail",
                                args=(station.council_id, station.internal_council_id),
                            ),
                        },
                    }
                    for station in stations
                ]
                + [
                    {
                        "type": "Feature",
                        "geometry": json.loads(residential_address.location.geojson)
                        if residential_address.location
                        else None,
                        "properties": {
                            "type": "residentialaddress",
                            "address": residential_address.address,
                            "color": station_colors[
                                (
                                    residential_address.council_id,
                                    residential_address.polling_station_id,
                                )
                            ],
                            "url": reverse(
                                "address_view", args=(residential_address.slug,)
                            ),
                        },
                    }
                    for residential_address in residential_addresses
                ],
            },
            content_type="application/geo+json",
        )


class PollingStationDetailView(DashboardMixin, DetailView):
    template_name = "dashboard/pollingstation_detail.html"
    queryset = PollingStation.objects.all()

    def get_object(self, queryset=None):
        return self.queryset.get(
            council_id=self.kwargs["council_pk"], internal_council_id=self.kwargs["id"]
        )
