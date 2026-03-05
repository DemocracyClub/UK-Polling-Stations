from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = (
        "2026-05-07/2026-03-05T12:00:58.887905/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T12:00:58.887905/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Fordingbridge Town Hall, 63 High Street, Fordingbridge, SP6 1AS
        if record.polling_place_id == "10163":
            record = record._replace(polling_place_easting="414713")
            record = record._replace(polling_place_northing="114134")

        # Totton & Eling Cricket Club, Southern Gardens, Ringwood Road, Totton, Southampton, SO40 8RW
        if record.polling_place_id == "10316":
            record = record._replace(polling_place_easting="435298")
            record = record._replace(polling_place_northing="113155")

        # Fawley Royal British Legion, 3 Exbury Road, Blackfield, Southampton, SO45 1XD
        if record.polling_place_id == "10294":
            record = record._replace(polling_place_easting="444266")
            record = record._replace(polling_place_northing="102155")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON, SO41 3NR
                "100060502037",  # THE GLEN, BUTTS ASH LANE, HYTHE, SOUTHAMPTON
                "10007451144",  # MOPLEY FARM, MOPLEY, LANGLEY, SOUTHAMPTON
                "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON
                "10007450313",  # HILLCROFT, IPERS BRIDGE, HOLBURY, SOUTHAMPTON
                "10007450771",  # GATEWOOD FARM, GATEWOOD HILL, BLACKFIELD, SOUTHAMPTON
                "10090350922",  # GREEN ROLLESTONE COPSE, ROLLESTONE ROAD, HOLBURY, SOUTHAMPTON
            ]
        ):
            return None

        return super().address_record_to_dict(record)
