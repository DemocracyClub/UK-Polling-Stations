from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = (
        "2024-07-04/2024-05-28T14:29:06.229594/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T14:29:06.229594/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Fordingbridge Town Hall, 63 High Street, Fordingbridge, SP6 1AS
        if record.polling_place_id == "9382":
            record = record._replace(polling_place_easting="414713")
            record = record._replace(polling_place_northing="114134")

        # Totton & Eling Cricket Club, Southern Gardens, Ringwood Road, Totton, Southampton, SO40 8RW
        if record.polling_place_id == "9608":
            record = record._replace(polling_place_easting="435298")
            record = record._replace(polling_place_northing="113155")

        # Fawley Royal British Legion, 3 Exbury Road, Blackfield, Southampton, SO45 1XD
        if record.polling_place_id == "9543":
            record = record._replace(polling_place_easting="444266")
            record = record._replace(polling_place_northing="102155")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON, SO41 3NR
            "100060502037",  # THE GLEN, BUTTS ASH LANE, HYTHE, SOUTHAMPTON
            "10007451144",  # MOPLEY FARM, MOPLEY, LANGLEY, SOUTHAMPTON
            "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON
            "10007450313",  # HILLCROFT, IPERS BRIDGE, HOLBURY, SOUTHAMPTON
            "10007450771",  # GATEWOOD FARM, GATEWOOD HILL, BLACKFIELD, SOUTHAMPTON
        ]:
            return None

        return super().address_record_to_dict(record)
