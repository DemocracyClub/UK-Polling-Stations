from uk_geo_utils.helpers import Postcode
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000031"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv2019peter.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv2019peter.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008075626"  # PE14AS -> PE14RA : 343A Eastfield Road, Peterborough
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10008072497"  # PE67AB -> PE67AE : Carpenters Cottage, Milton Park, Peterborough
        ]:
            rec["accept_suggestion"] = False

        if Postcode(record.addressline6).with_space == "PE7 8PP":
            return None

        return rec
