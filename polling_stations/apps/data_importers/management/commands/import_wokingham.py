from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = "2021-04-12T09:10:21.537410/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-12T09:10:21.537410/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "14008163",  # LOWER COTTAGE, WHITE HORSE LANE, FINCHAMPSTEAD, WOKINGHAM
            "10094223552",  # 4 SHEERLANDS ROAD, ARBORFIELD
            "14006244",  # FIELD VIEW, MOLE ROAD, SINDLESHAM, WOKINGHAM
            "14063909",  # MAYS HILL LODGE, BEECH HILL ROAD, SPENCERS WOOD, READING
            "10032929468",  # LANE END FARM HOUSE, SHINFIELD ROAD, SHINFIELD, READING
        ]:
            return None

        if record.addressline6 in [
            "RG2 9LG",
            "RG6 4AG",
            "RG7 1NL",
            "RG41 4EL",
            "RG10 9HN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Civic Offices Shute End Wokingham Berkshire RG40 1WH
        if record.polling_place_id == "2740":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
