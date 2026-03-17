from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WSK"
    addresses_name = (
        "2026-05-07/2026-03-17T15:32:06.667126/Democracy_Club__07May2026 (1).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T15:32:06.667126/Democracy_Club__07May2026 (1).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091029230",  # 23 BURY ROAD, NEWMARKET
            "200001370253",  # 27 BURY ROAD, NEWMARKET
            "10009749005",  # BLUE DOORS FARM, COWLINGE, NEWMARKET
            "10095885133",  # THE GARDEN FLAT 12 THE AVENUE, NEWMARKET
            "100091370064",  # PEGASUS STABLES SNAILWELL ROAD, NEWMARKET
        ]:
            return None

        if record.addressline6 in [
            # split
            "CB9 9HN",
            # looks wrong
            "CB8 7DJ",
            "CB8 9YF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warning checked and no correction required:
        # WARNING: Polling station The Beeches (19036) is in East Cambridgeshire District Council (ECA)

        # more accurate point for:
        # East Town Park Visitor Centre, Coupals Road, Haverhill, CB9 7UW
        if record.polling_place_id == "21216":
            record = record._replace(polling_place_easting="568610")
            record = record._replace(polling_place_northing="244831")

        return super().station_record_to_dict(record)
