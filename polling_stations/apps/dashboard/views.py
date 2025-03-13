import json
import operator
from functools import reduce

from addressbase.models import Address
from councils.models import Council
from data_finder.helpers import RoutingHelper
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from pollingstations.models import PollingStation
from uk_geo_utils.helpers import Postcode


class IndexView(ListView):
    queryset = Council.objects.select_related("dataquality")
    template_name = "dashboard/council_list.html"


class CouncilDetailView(DetailView):
    queryset = Council.objects.all()
    template_name = "dashboard/council_detail.html"

    def get_context_data(self, object, **kwargs):
        context = super().get_context_data(object=object, **kwargs)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT postcode, st_maxdistance(multipoint, multipoint)::int AS maxdistance
                FROM (
                    SELECT aa.postcode, st_transform(st_collect(aa.location), 27700) AS multipoint
                    FROM addressbase_address aa JOIN addressbase_uprntocouncil uc
                    ON aa.uprn = uc.uprn
                    WHERE uc.lad = %s AND uc.polling_station_id != ''
                    GROUP BY aa.postcode
                ) AS subquery
                WHERE multipoint IS NOT NULL
                ORDER BY maxdistance DESC
                LIMIT 20;
            """,
                (object.geography.gss,),
            )
            context["postcodes_by_diameter"] = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT aa.postcode, max(st_distance(
                        st_transform(ps.location, 27700),
                        st_transform(COALESCE(aa.location), 27700)
                    )::int) AS distance
                FROM
                    addressbase_address aa
                    JOIN addressbase_uprntocouncil uc
                        ON aa.uprn = uc.uprn
                    JOIN pollingstations_pollingstation ps
                        ON uc.polling_station_id = ps.internal_council_id
                    JOIN councils_councilgeography cg
                        ON ps.council_id = cg.council_id
                WHERE
                    cg.council_id = %s
                    AND ps.location IS NOT NULL
                GROUP BY aa.postcode
                ORDER BY distance DESC
                LIMIT 50;
                """,
                (object.council_id,),
            )

            context["distances_to_stations"] = cursor.fetchall()

        context["pollingstation_list"] = PollingStation.objects.filter(
            council=object
        ).order_by("internal_council_id")

        return context


class PostCodeView(TemplateView):
    template_name = "dashboard/postcode.html"

    def get_context_data(self, postcode, **kwargs):
        postcode = Postcode(postcode)
        addresses = Address.objects.filter(postcode=postcode.with_space)
        unassigned_addresses = [a for a in addresses if not a.polling_station_id]
        addresses = [a for a in addresses if a.polling_station_id]
        return {
            "postcode": postcode,
            "addresses": addresses,
            "unassigned_addresses": unassigned_addresses,
            "routing_helper": RoutingHelper(postcode),
        }


class PostCodeGeoJSONView(View):
    station_colors = ["purple", "red", "blue", "yellow", "green", "pink", "orange"]

    def get(self, request, postcode):
        postcode = Postcode(postcode)
        addresses = Address.objects.filter(postcode=postcode.with_space)
        station_ids = sorted({(a.council_id, a.polling_station_id) for a in addresses})
        if station_ids:
            stations = PollingStation.objects.filter(
                reduce(
                    operator.or_,
                    (
                        Q(
                            council_id=council_id,
                            internal_council_id=internal_council_id,
                        )
                        for council_id, internal_council_id in station_ids
                    ),
                )
            )
        else:
            stations = PollingStation.objects.none()
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
                            "address": station.address + ", " + station.postcode,
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
                        "geometry": json.loads(address.location.geojson)
                        if address.location
                        else None,
                        "properties": {
                            "type": "residentialaddress",
                            "address": address.address + ", " + address.postcode,
                            "color": station_colors[
                                (
                                    address.council_id,
                                    address.polling_station_id,
                                )
                            ]
                            if address.polling_station_id
                            else "white",
                            "uprn": address.uprn,
                            "polling_station_id": address.polling_station_id,
                            "url": reverse("address_view", args=(address.uprn,)),
                        },
                    }
                    for address in addresses
                ],
            },
            content_type="application/geo+json",
        )


class PollingStationDetailView(DetailView):
    template_name = "dashboard/pollingstation_detail.html"
    queryset = PollingStation.objects.all()

    def get_object(self, queryset=None):
        return self.queryset.get(
            council_id=self.kwargs["council_pk"], internal_council_id=self.kwargs["id"]
        )
