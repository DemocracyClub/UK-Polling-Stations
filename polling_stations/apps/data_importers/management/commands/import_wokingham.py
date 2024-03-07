from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2024-05-02/2024-03-07T15:21:25.732078/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T15:21:25.732078/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "14023395",  # SCHOOL BUNGALOW, WESTERN AVENUE, WOODLEY, READING
            "14006686",  # THE LODGE, BEARWOOD COLLEGE, WINNERSH, WOKINGHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RG2 9LG",
            "RG7 1NL",
            # looks wrong
            "RG7 1PS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # adding point for: St John’s Church Centre, Church Road, Woodley, Reading, RG5 4QN
        if record.polling_place_id == "3700":
            record = record._replace(polling_place_easting="476847")
            record = record._replace(polling_place_northing="173732")

        # adding point for: St Sebastian`s Memorial Hall, Nine Mile Ride, Wokingham, RG40 3BA
        if record.polling_place_id == "3695":
            record = record._replace(polling_place_easting="483182")
            record = record._replace(polling_place_northing="165582")

        return super().station_record_to_dict(record)
