from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2022-05-05/2022-02-22T14:39:34.210989/Democracy_Club__05May2022 (1).tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-22T14:39:34.210989/Democracy_Club__05May2022 (1).tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Sutton Village Church, Herbert Street
        if record.polling_place_id == "4714":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        # Newton Childrens Centre
        if record.polling_place_id == "4831":
            record = record._replace(polling_place_easting="357498")
            record = record._replace(polling_place_northing="395524")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "39097215",  # 8 PARK AVENUE NORTH, NEWTON-LE-WILLOWS, WA12 8HL
        ]:
            return None
        if record.addressline6 in [
            "WA9 3RR",
            "WA9 3UF",
            "WA10 1HT",
        ]:
            return None
        return super().address_record_to_dict(record)
