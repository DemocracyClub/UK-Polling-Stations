import datetime

from councils.models import Council
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from file_uploads.models import ElectionReturn
from pollingstations.models import PollingStation, VisibilityChoices

# A handful of real Stroud district towns/villages with plausible (fake)
# polling place venues, so local testing has something recognisable rather
# than generic Faker output.
STROUD_STATIONS = [
    ("Stroud", "Stroud Subscription Rooms", "GL5 1AE", (51.7454, -2.2159)),
    ("Stroud", "Stroud Valleys Community TV Hall", "GL5 1JQ", (51.7469, -2.2192)),
    ("Nailsworth", "Nailsworth Town Hall", "GL6 0DU", (51.6942, -2.2185)),
    ("Dursley", "Dursley Baptist Church Hall", "GL11 4AJ", (51.6837, -2.3562)),
    ("Stonehouse", "Stonehouse Town Hall", "GL10 2NA", (51.7539, -2.2761)),
    ("Painswick", "Painswick Town Hall", "GL6 6QN", (51.7897, -2.1919)),
    ("Minchinhampton", "Minchinhampton Market House", "GL6 9BN", (51.6975, -2.1653)),
    ("Chalford", "Chalford Community Centre", "GL6 8DS", (51.7269, -2.1499)),
    ("Cam", "Cam Woodfield Junior School", "GL11 5LT", (51.7076, -2.3733)),
    ("Wotton-under-Edge", "Wotton-under-Edge Civic Centre", "GL12 7BT", (51.6379, -2.3517)),
    ("Berkeley", "Berkeley Town Hall", "GL13 9BG", (51.6899, -2.4574)),
    ("Rodborough", "Rodborough Community Hub", "GL5 3SU", (51.7373, -2.2261)),
]


class Command(BaseCommand):
    help = (
        "Populate the local database with fake polling station and "
        "post-election return data for Stroud District Council, so the "
        "election-return forms can be exercised locally."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--council-id",
            default="STO",
            help="council_id to use (defaults to Stroud District Council's 'STO')",
        )

    def handle(self, *args, **options):
        council = Council.objects.get(council_id=options["council_id"])

        created_stations = 0
        for i, (town, venue, postcode, (lat, lng)) in enumerate(STROUD_STATIONS, start=1):
            _, created = PollingStation.objects.get_or_create(
                council=council,
                internal_council_id=f"STO-{i:02d}",
                defaults={
                    "postcode": postcode,
                    "address": f"{venue}\n{town}\nGloucestershire",
                    "location": Point(x=lng, y=lat, srid=4326),
                    "visibility": VisibilityChoices.PUBLISHED,
                },
            )
            created_stations += int(created)

        election_return, er_created = ElectionReturn.objects.get_or_create(
            council=council,
            election_id="local.stroud.2026-05-07",
            defaults={
                "election_title": "Stroud District Council local election",
                "poll_open_date": datetime.date(2026, 5, 7),
                "requires_voter_id": "EA-2022",
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Stroud District Council ({council.council_id}): "
                f"{created_stations} new polling station(s) created "
                f"({council.pollingstation_set.count()} total).\n"
                f"Election return {'created' if er_created else 'already existed'}: "
                f"{election_return.election_title} ({election_return.election_id}).\n\n"
                "Visit (while logged in as an active user):\n"
                f"  /uploads/election_returns/{council.council_id}/\n"
                f"  /uploads/election_returns/{council.council_id}/{election_return.election_id}/\n"
            )
        )
