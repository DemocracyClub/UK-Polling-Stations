from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2026-05-07/2026-02-05T14:40:25.253534/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T14:40:25.253534/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "14023395",  # SCHOOL BUNGALOW, WESTERN AVENUE, WOODLEY, READING
            "14000374",  # OAKLEY COTTAGE, BARGE LANE, SWALLOWFIELD, READING
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "RG7 1PS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # adding point for: St John’s Church Centre, Church Road, Woodley, Reading, RG5 4QN
        if record.polling_place_id == "4976":
            record = record._replace(polling_place_easting="476847")
            record = record._replace(polling_place_northing="173732")

        # adding point for: St Sebastian`s Memorial Hall, Nine Mile Ride, Wokingham, RG40 3BA
        if record.polling_place_id == "5160":
            record = record._replace(polling_place_easting="483182")
            record = record._replace(polling_place_northing="165582")

        return super().station_record_to_dict(record)
