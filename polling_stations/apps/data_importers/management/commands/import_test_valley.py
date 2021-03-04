from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TES"
    addresses_name = (
        "2021-03-03T11:17:35.093086/Test Valley Democracy_Club__06May2021 (1).tsv"
    )
    stations_name = (
        "2021-03-03T11:17:35.093086/Test Valley Democracy_Club__06May2021 (1).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091683563",  # FISHERMANS LODGE MILL LANE, WHERWELL, ANDOVER
            "10023629571",  # FLAT D, CHANTRY LODGE, CHANTRY STREET, ANDOVER
        ]:
            return None

        if record.addressline6 in ["SP11 0HB", "SO51 6EB"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "9944"
        ):  # Andover Bowling Club Recreation Road Andover SP10 1HL
            record = record._replace(polling_place_easting="436873")
            record = record._replace(polling_place_northing="145802")

        return super().station_record_to_dict(record)
