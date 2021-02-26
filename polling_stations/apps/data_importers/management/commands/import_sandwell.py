from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2021-02-25T09:04:33.366338/Democracy Club Polling Place Lookup 6 May2021.tsv"
    )
    stations_name = (
        "2021-02-25T09:04:33.366338/Democracy Club Polling Place Lookup 6 May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "18846"
        ):  # Hallam Street Methodist Church, Community Room, Lewisham Street, West Bromwich, B71 4HJ
            record = record._replace(polling_place_postcode="B71 4HG")

        if (
            record.polling_place_id == "18865"
        ):  # St Philips Church Hall, Beeches Road, West Bromwich, B70 7PF
            record = record._replace(polling_place_postcode="B70 6JA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in [
            "10093004484",  # FLAT THE DOVECOTE HILL TOP, WEST BROMWICH B70 0SD
            "100071578415",  # 622A BEARWOOD ROAD, SMETHWICK B664DP
            "32072080",  # 251 HOLYHEAD ROAD, WEDNESBURY WS107DQ
            "32072081",  # 253 HOLYHEAD ROAD, WEDNESBURY WS107DQ
        ]:
            return None

        if record.addressline6 in [
            "B65 0BS",
            "DY4 9NB",
            "B70 8DB",
            "B67 7EP",
            "B64 7JA",
            "B64 5NX",
            "B69 4DH",
            "B69 3FF",
        ]:
            return None

        if record.post_code == "B7O 9LG":
            rec["postcode"] = "B709LG"
        if record.post_code == "B70 OSH":
            rec["postcode"] = "B700SH"
        if record.post_code == "B68 OLH":
            rec["postcode"] = "B680LH"

        return rec
