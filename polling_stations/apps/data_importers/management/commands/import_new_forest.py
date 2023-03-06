from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = (
        "2023-05-04/2023-03-06T10:28:37.564607/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-06T10:28:37.564607/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # corrections from council
        if (
            record.polling_place_id == "8818"
        ):  # Fordingbridge Town Hall, 63 High Street, Fordingbridge, SP6 1AS
            record = record._replace(polling_place_easting="414713")
            record = record._replace(polling_place_northing="114134")
        if (
            record.polling_place_id == "8963"
        ):  # Totton & Eling Cricket Club, Southern Gardens, Ringwood Road, Totton, Southampton, SO40 8RW
            record = record._replace(polling_place_easting="435298")
            record = record._replace(polling_place_northing="113155")

        return super().station_record_to_dict(record)

    #
    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON, SO41 3NR
        ]:
            return None

        return super().address_record_to_dict(record)
