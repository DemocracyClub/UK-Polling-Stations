from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWA"
    addresses_name = (
        "2021-03-26T10:37:06.912765/North Warwickshire Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-26T10:37:06.912765/North Warwickshire Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Dordon Village Hall Browns Lane Dordon B78 1LT
        if record.polling_place_id == "3738":
            record = record._replace(polling_place_postcode="B78 1TR")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001177416",  # WARREN FARM HOUSE, KINWALSEY LANE, MERIDEN, COVENTRY
            "100071230625",  # GRIFFIN INN, COLESHILL ROAD, SHUSTOKE, COLESHILL, BIRMINGHAM
        ]:
            return None

        if record.addressline6 in [
            "B46 2NX",
            "CV9 1AX",
            "CV9 2HS",
            "B46 1AA",
            "B46 1BB",
            "B46 2HS",
            "CV10 0SL",
        ]:
            return None

        return super().address_record_to_dict(record)
