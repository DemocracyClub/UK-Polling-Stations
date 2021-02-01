from django.contrib.gis.geos import MultiPolygon, Polygon, Point
from faker import Faker
from uk_geo_utils.models import Onspd

from addressbase.tests.factories import AddressFactory, UprnToCouncilFactory
from councils.tests.factories import CouncilFactory
from pollingstations.tests.factories import PollingStationFactory

fake = Faker("en_GB")
fake.seed_instance(0)


class ImpossiblePostcodeError(Exception):
    pass


def get_unique_point_in_extent(extent):
    """
    Extent should be (MinX, MinY, MaxX, MaxY)
    i.e. like returned by GEOSGeometry extent() method
    """
    if extent[2] - extent[0] <= 2 or extent[3] - extent[1] <= 2:
        raise ValueError
    min_x = extent[0] + 1
    min_y = extent[1] + 1
    max_x = extent[2] - 1
    max_y = extent[3] - 1
    x = fake.unique.pyfloat(min_value=min_x, max_value=max_x)
    y = fake.unique.pyfloat(min_value=min_y, max_value=max_y)
    return Point(x, y)


class PostcodeBuilder:
    """
    Builder for creating postcodes to test data finder and api
    Trying to control for the following variables:
        - Postcode contained by one or two councils
        - Postcode contained by one or two nations
        - Postcode contains addressbase addresses with a polling station assigned
        - Postcode contains addressbase addresses with a polling station unassigned
        - Postcode is in ONSPD
    """

    def __init__(self, multiple_councils=False, nations=("E")):
        """
        Make a class with a postcode and a council.
        Give the council an area.
        """
        self.multiple_councils = multiple_councils
        self.nations = nations
        self.postcode = fake.unique.postcode()
        self.geometry = MultiPolygon(
            Polygon(((20, 20), (20, 40), (40, 40), (40, 20), (20, 20)))
        )
        self.councils = self.make_councils()
        self.stations = []
        self.addresses = []
        self.unassigned_addresses = []

    def with_assigned_addresses(self):
        for council in self.councils:
            polling_station = PollingStationFactory(council=council)
            self.stations.append(polling_station)
            address = self.create_address(
                council, polling_station_id=polling_station.internal_council_id
            )
            self.addresses.append(address)
        return self

    def with_unassigned_addresses(self):
        for council in self.councils:
            address = self.create_address(council)
            self.unassigned_addresses.append(address)
        return self

    def create_address(self, council, polling_station_id=""):
        """Only works if self.geometry is a box."""
        overlap = self.geometry.intersection(council.area)
        address = AddressFactory(
            location=get_unique_point_in_extent(overlap.extent), postcode=self.postcode
        )
        UprnToCouncilFactory(
            uprn=address, lad=council.council_id, polling_station_id=polling_station_id
        )
        return address

    def in_onspd(self):
        Onspd.objects.update_or_create(pcds=self.postcode)
        return self

    def make_councils(self):
        # Make a council that contains the postcode
        if len(self.nations) == 1 and not self.multiple_councils:
            councils = [
                CouncilFactory(
                    council_id=f"{self.nations[0]}{fake.unique.pyint(min_value=10000000, max_value=99999999)}",
                    area=MultiPolygon(
                        Polygon(((0, 0), (0, 50), (50, 50), (50, 0), (0, 0)))
                    ),
                )
            ]
        # Make two councils which both intersect the postcode
        elif len(self.nations) == 1 and self.multiple_councils:
            councils = [
                CouncilFactory(
                    council_id=f"{self.nations[0]}{fake.unique.pyint(min_value=10000000, max_value=99999999)}",
                    area=MultiPolygon(
                        Polygon(((0, 0), (0, 50), (30, 50), (30, 0), (0, 0)))
                    ),
                ),
                CouncilFactory(
                    council_id=f"{self.nations[0]}{fake.unique.pyint(min_value=10000000, max_value=99999999)}",
                    area=MultiPolygon(
                        Polygon(((30, 0), (30, 50), (50, 50), (50, 0), (30, 0)))
                    ),
                ),
            ]
        # Make two councils in two nations.
        elif len(self.nations) == 2 and self.multiple_councils:
            councils = [
                CouncilFactory(
                    council_id=f"{self.nations[0]}{fake.unique.pyint(min_value=10000000, max_value=99999999)}",
                    area=MultiPolygon(
                        Polygon(((0, 0), (0, 50), (30, 50), (30, 0), (0, 0)))
                    ),
                ),
                CouncilFactory(
                    council_id=f"{self.nations[1]}{fake.unique.pyint(min_value=10000000, max_value=99999999)}",
                    area=MultiPolygon(
                        Polygon(((30, 0), (30, 50), (50, 50), (50, 0), (30, 0)))
                    ),
                ),
            ]
        # Other scenarios are impossible:
        # eg >2 nations, >1 nation plus single council.
        else:
            raise ImpossiblePostcodeError  # TODO make it useful

        return councils
