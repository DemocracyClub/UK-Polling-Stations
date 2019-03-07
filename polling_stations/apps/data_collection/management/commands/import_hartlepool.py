from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from data_collection.addresshelpers import format_residential_address


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000001"
    addresses_name = "local.2019-05-02/Version 1/Polling Station Address Information 02 May 2019 Hartlepool.csv"
    stations_name = "local.2019-05-02/Version 1/Polling Station Address Information 02 May 2019 Hartlepool.csv"
    elections = ["local.2019-05-02"]

    # Hartlepool use Xpress, but they've provided a slightly trimmed down
    # version of the export. We need to customise a bit..
    station_uprn_field = None

    def station_record_to_dict(self, record):

        if record.polling_place_id == "8017":
            record = record._replace(polling_place_name="Warrior Park Care Home")
            record = record._replace(polling_place_address_1="Queen Street")
            record = record._replace(polling_place_address_2="Seaton Carew")
            record = record._replace(polling_place_address_3="Stockport")
            record = record._replace(polling_place_address_4="Hartlepool")
            record = record._replace(polling_place_postcode="TS25 1EZ")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.191945, 54.664709, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.post_code.strip() == "":
            return None
        address = format_residential_address(
            [
                record.addressline1,
                record.addressline2,
                record.addressline3,
                record.addressline4,
            ]
        )
        uprn = getattr(record, self.residential_uprn_field).strip().lstrip("0")
        postcode = record.post_code.strip()
        ret = {
            "address": address.strip(),
            "postcode": postcode,
            "polling_station_id": getattr(record, self.station_id_field).strip(),
            "uprn": uprn,
        }

        # corrections
        if postcode in ["TS25 2HE", "TS24 0HJ"]:
            return None

        if uprn in ["10090068484", "10009734034", "100110786034"]:
            ret["accept_suggestion"] = True

        if uprn in ["100110673453", "100110673049"]:
            ret["accept_suggestion"] = False

        return ret
