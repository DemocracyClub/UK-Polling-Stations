from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000011"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019know.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019know.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "40038051":
            return None

        if record.addressline1 == "14A Katherine Walk":
            return None

        if record.addressline6 == "L34 6JQ":
            return None

        if uprn in [
            "40061353",
            "40056575",
            "40008720",  # L266LB -> L266LA
            "40008721",  # L266LB -> L266LA
            "40008722",  # L266LB -> L266LA
            "40008723",  # L266LB -> L266LA
            "40008724",  # L266LB -> L266LA
            "40008729",  # L266LB -> L267YE
            "40076082",  # L266LB -> L266LA
            "40076083",  # L266LB -> L266LA
            "40083391",  # L321BB -> L321BJ
            "40038051",  # L364HS -> L365ST
            "40076030",  # L365UZ -> L365UY
            "40042146",  # L365YR -> L365UY
            "40074803",  # L365YR -> L365UY
            "40056755",  # L368EL -> L368HW
            "40056758",  # L368EL -> L368HW
        ]:
            rec["accept_suggestion"] = True

        return rec
