from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = "2021-03-16T07:43:19.094610/wandsworth_deduped.tsv"
    stations_name = "2021-03-16T07:43:19.094610/wandsworth_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094188577",  # DL ELECTRICAL SUPPLIES MITCHAM LIMITED, GROUND FLOOR RIGHT HAND SIDE 1A TOTTERDOWN STREET, LONDON
            "121014813",  # 2A COMBEMARTIN ROAD, LONDON
            "10070240964",  # FLAT D23B, DU CANE COURT, BALHAM HIGH ROAD, LONDON
            "10094188577",  # 2A COMBEMARTIN ROAD, LONDON
            "100022680823",  # 14A PRINCE OF WALES MANSIONS PRINCE OF WALES DRIVE, LONDON
            "10094189386",  # FLAT 1 111 UPPER TOOTING ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            "SW15 4HT",
            "SW15 3HY",
            "SW18 2QZ",
            "SW17 7BB",
            "SW11 3NA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St John's Hill Residents Centre Peabody Estate (entrance from St John`s Hill only) London SW11 1UZ
        if record.polling_place_id == "8054":
            record = record._replace(polling_place_easting="527229")
            record = record._replace(polling_place_northing="175282")

        return super().station_record_to_dict(record)
