from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAC"
    addresses_name = (
        "2025-05-01/2025-04-02T08:39:51.055604/Democracy_Club__01May2025 (8).tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-02T08:39:51.055604/Democracy_Club__01May2025 (8).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: Nash Mills Village Hall, 4 Lower Road, Nash Mills, HP3 8RU
        if record.polling_place_id == "3664":
            record = record._replace(polling_place_easting="507211")
            record = record._replace(polling_place_northing="204366")

        # address correction for: St Pauls Church Hall, 39 Meadow Road, Hemel Hempstead, HP3 8AJ
        if record.polling_place_id == "3594":
            record = record._replace(polling_place_name="St Paul's Church")
            record = record._replace(polling_place_address_1="Solway")
            record = record._replace(polling_place_address_4="Hemel Hempstead")
            record = record._replace(polling_place_postcode="HP2 5QN")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095348524",  # LAKE VIEW, PIX FARM LANE, HEMEL HEMPSTEAD
            "100081113670",  # OLD FISHERY COTTAGE, OLD FISHERY LANE, HEMEL HEMPSTEAD
            "100081113665",  # BARGEMOOR, OLD FISHERY LANE, HEMEL HEMPSTEAD
            "100081113665",  # BARGEMOOR, OLD FISHERY LANE, HEMEL HEMPSTEAD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "HP2 4AP",
            "HP2 6JN",
            "HP2 4QY",
            # looks wrong
            "HP3 9DJ",
            "HP1 2RE",
            "HP23 5BE",
        ]:
            return None

        return super().address_record_to_dict(record)
