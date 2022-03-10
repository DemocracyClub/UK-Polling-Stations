from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRD"
    addresses_name = (
        "2022-05-05/2022-03-10T15:15:55.571130/Democracy_Club__05May2022-2.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T15:15:55.571130/Democracy_Club__05May2022-2.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # St John`s Church South Street Keighley BD22 7BU
        if record.polling_place_id == "28550":
            record = record._replace(polling_place_easting="405613")
            record = record._replace(polling_place_northing="439897")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100051942648",
            "10010571811",
            "10010571812",
            "10090402080",
            "10090402777",
            "10090978516",
            "100051268913",
            "10090404116",
            "100051268917",
            "10091675520",  # 12 BRIGGS WAY, BRADFORD
            "10091675521",  # 10 BRIGGS WAY, BRADFORD
        ]:
            return None

        if record.addressline6 in [
            "BD13 3SD",
            "BD1 1NE",
            "BD1 1SX",
            "BD16 1NT",
            "BD15 7WB",
            "BD7 4RA",
            "LS29 6QJ",
            "BD9 6AS",
            "BD10 8LL",
            "BD21 5QF",
            "BD1 4AB",
        ]:
            return None

        return super().address_record_to_dict(record)
