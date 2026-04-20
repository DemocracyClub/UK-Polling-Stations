from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2026-05-07/2026-03-30T09:35:47.578722/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-30T09:35:47.578722/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "77176372",  # 12 HAVERS ROAD, MANCHESTER
            "77123789",  # 2 ALMOND STREET, MANCHESTER
            "77123796",  # 2 DAVY STREET, MANCHESTER
            "10024146870",  # SECOND FLOOR FLAT 76 RICHMOND GROVE, MANCHESTER
            "10024146868",  # GROUND FLOOR FLAT 76 RICHMOND GROVE, MANCHESTER
            "10024146869",  # FIRST FLOOR FLAT 76 RICHMOND GROVE, MANCHESTER
        ]:
            return None

        if record.addressline6 in [
            # splits
            "M12 5PR",
            "M14 5DQ",
            "M14 5LN",
            "M22 8BE",
            "M8 9AE",
            # looks wrong
            "M19 3NW",
            "M22 5BL",
            "M8 4RB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # change requested by council
        # Old station: Sandilands Primary School, Infant Department, Wendover Road, Brooklands, Manchester, M23 9JX
        # New station (already in db): Church of the Nazarene, Wendover Road, Brooklands, Manchester, M23 9FN
        if record.polling_place_id == "15420":
            record = record._replace(
                polling_place_name="Church of the Nazarene",
                polling_place_address_1="Wendover Road",
                polling_place_address_2="",
                polling_place_address_3="Brooklands",
                polling_place_address_4="Manchester",
                polling_place_postcode="M23 9FN",
                polling_place_uprn="",
                polling_place_easting="379820",
                polling_place_northing="389788",
            )

        return super().station_record_to_dict(record)
