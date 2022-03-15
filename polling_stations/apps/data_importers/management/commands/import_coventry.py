from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = (
        "2022-05-05/2022-03-15T18:03:40.948418/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-15T18:03:40.948418/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095509721",  # FLAT ABOVE BROAD LANE TRADING ESTATE BANNER LANE, COVENTRY
            "10091718353",  # 112 WOODWAY LANE, COVENTRY
            "10095510480",  # FIRST FLOOR FLAT 658 FOLESHILL ROAD, COVENTRY
        ]:
            return None

        if record.addressline6 in [
            "CV2 1FX",
            "CV2 4GA",
            "CV4 9LP",
            "CV4 9YJ",
            "CV6 5NU",
            "CV7 8NJ",
            "CV3 1QH",
            "CV2 1TA",
            "CV2 2XL",
            "CV2 2XJ",
            "CV6 4DD",
            "CV4 7AL",
        ]:
            return None

        return super().address_record_to_dict(record)
