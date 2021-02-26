from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = "2021-02-24T12:13:04.627288/Democracy_Club__06May2021.tsv"
    stations_name = "2021-02-24T12:13:04.627288/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        # corrections from council
        if (
            record.polling_place_id == "8374"
        ):  # Fordingbridge Town Hall, 63 High Street, Fordingbridge, SP6 1AS
            record = record._replace(polling_place_easting="414713.35")
            record = record._replace(polling_place_northing="114134.91")
        if (
            record.polling_place_id == "8523"
        ):  # Totton & Eling Cricket Club, Southern Gardens, Ringwood Road, Totton, Southampton, SO40 8RW
            record = record._replace(polling_place_easting="435321.7")
            record = record._replace(polling_place_northing="113089.68")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093932670",  # NEWTOWN LANE FARM, NEWTOWN LANE, MOCKBEGGAR, RINGWOOD, BH24 3NN
            "100062214501",  # FORTUNE CENTRE OF RIDING THERAPY, WOOTON HALL FARM, TIPTOE ROAD, NEW MILTON, BH25 5SJ
            "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON, SO41 3NR
        ]:
            return None

        if record.addressline6 in ["SO45 4PA"]:
            return None

        return rec
