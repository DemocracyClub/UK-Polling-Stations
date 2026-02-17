from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = (
        "2026-05-07/2026-02-05T14:50:21.960578/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T14:50:21.960578/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # council-approved more accurate coordinates for:
        # Bishopstoke Methodist Church, Sedgwick Road, Bishopstoke, Eastleigh SO50 6FH
        if record.polling_place_id == "6408":
            record = record._replace(
                polling_place_easting="446888",
                polling_place_northing="119531",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091134664",  # CHERRYWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134663",  # LARCHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134662",  # ASHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134661",  # SPINDLEWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10009640001",  # OAK COTTAGE, ALLINGTON LANE, FAIR OAK, EASTLEIGH
        ]:
            return None

        if record.addressline6 in [
            # split
            "SO31 8AF",
            "SO30 0DF",
        ]:
            return None

        return super().address_record_to_dict(record)
