from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "HMF"
    addresses_name = "2024-05-02/2024-02-22T12:16:44.125848/Eros_SQL_Output008.csv"
    stations_name = "2024-05-02/2024-02-22T12:16:44.125848/Eros_SQL_Output008.csv"
    elections = ["2024-05-02"]

    # WARNING: Polling station Edward Woods Community Centre (54-edward-woods-community-centre) is in
    # Royal Borough of Kensington and Chelsea (KEC) but target council is London Borough of Hammersmith and Fulham (HMF)
    # Above warning was checked and no correction is needed

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()

        if uprn in [
            "34146774",  # THIRD FLOOR FLAT 95 HAMMERSMITH GROVE, LONDON
            "34140773",  # MITRE WHARF MOORINGS SCRUBS LANE, LONDON
            "34003087",  # 4 STEVENTON ROAD, LONDON
            "34077511",  # FIRST FLOOR 35 QUERRIN STREET, LONDON
            "34077512",  # GROUND FLOOR 35 QUERRIN STREET, LONDON
            "34152960",  # UNIT C MAIN ENTRANCE CHARING CROSS HOSPITAL FULHAM PALACE ROAD, LONDON
            "34012656",  # 26 ALDENSLEY ROAD, LONDON
            "34012840",  # 142 DALLING ROAD, LONDON
            "34131964",  # 147 HAZLEBURY ROAD, LONDON
            "34076261",  # 110A TOWNMEAD ROAD, LONDON
            "34076242",  # 25 KILKIE STREET, LONDON
        ]:
            return None

        if record.housepostcode in [
            # splits
            "SW6 7JZ",
            "SW6 7PT",
            "SW6 2AA",  # BAGLEYS LANE, LONDON
            "SW6 2TS",  # 123-125 WANDSWORTH BRIDGE ROAD, LONDON
            "SW6 7HG",  # RYLSTON ROAD, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
