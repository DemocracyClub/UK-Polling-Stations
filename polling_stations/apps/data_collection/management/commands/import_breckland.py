from uk_geo_utils.helpers import Postcode
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000143"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019breck.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019breck.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if record.polling_place_id in ["8277", "8377", "8521"]:
            # The E/N points are the wrong way round for these 3
            # perform the old switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        if record.polling_place_id == "8440":
            # this one is just miles off
            # remove it and fall back to geocoding by postcode
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10011992099":
            rec["postcode"] = "PE32 2DQ"

        if Postcode(record.addressline6).with_space == "IP24 1QS":
            return None

        if (
            record.addressline1 == "122/123"
            and record.addressline2 == "Green Lane Quidenham"
            and record.addressline3 == "Norwich"
            and record.addressline4 == "Norfolk"
        ):
            return None

        if uprn in [
            "10011984733"  # PE322NB -> PE322RP : Lilac Cottages, 2 Litcham Road, Beeston, Kings Lynn, Norfolk
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100091305655",  # NR171DY -> NR171EA : Red Lodge, Watton Road, Shropham, Attleborough, Norfolk
            "100090787475",  # IP257AX -> IP257BL : Flint Cottage, Hale Road, Ashill, Thetford, Norfolk
        ]:
            rec["accept_suggestion"] = False

        return rec
