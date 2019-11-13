from uk_geo_utils.helpers import Postcode
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000031"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019peter.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019peter.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7914":
            record = record._replace(polling_place_postcode="PE7 8HG")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008075626"  # PE14AS -> PE14RA : 343A Eastfield Road, Peterborough
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10008072497",  # PE67AB -> PE67AE : Carpenters Cottage, Milton Park, Peterborough
            "10008065034",  # PE93BY -> PE93BN : High Farm, Main Street, Southorpe, Stamford
            "10008064909",  # PE67EN -> PE67DU : Addys Barn, King Street, Helpston, Peterborough
        ]:
            rec["accept_suggestion"] = False

        if Postcode(record.addressline6).with_space in ("PE7 8PP", "PE3 6HP"):
            return None

        return rec
