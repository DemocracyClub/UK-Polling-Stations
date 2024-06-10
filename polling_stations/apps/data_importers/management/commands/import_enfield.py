from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENF"
    addresses_name = (
        "2024-07-04/2024-06-10T14:11:55.517464/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-10T14:11:55.517464/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Enfield Highway Community Centre, 117 Hertford Road, Enfield
        if record.polling_place_id == "9337":
            record = record._replace(polling_place_easting="535189")
            record = record._replace(polling_place_northing="197091")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "207184074",  # MAINYARD STUDIOS, 58B ALEXANDRA ROAD, ENFIELD
            "207104137",  # BUSH HILL COTTAGE 20 BUSH HILL, SOUTHGATE
            "207037892",  # THE LODGE, SWEET BRIAR WALK, LONDON
            "207158629",  # NORTH LODGE, TRENT PARK, FERNY HILL, BARNET
        ]:
            return None

        if record.addressline6 in [
            # split
            "N21 2DS",
            "N18 2EH",
            "N9 9RP",
            # suspect
            "EN2 8GJ",
            "N13 4HE",
            "EN3 7EH",
            "EN1 1GL",
        ]:
            return None

        return super().address_record_to_dict(record)
