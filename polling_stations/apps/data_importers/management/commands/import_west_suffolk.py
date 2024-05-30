from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WSK"
    addresses_name = (
        "2024-07-04/2024-05-30T14:06:54.881649/Democracy_Club__04July2024 (3).tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T14:06:54.881649/Democracy_Club__04July2024 (3).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091029230",  # 23 BURY ROAD, NEWMARKET
            "200001370253",  # 27 BURY ROAD, NEWMARKET
            "10094064664",  # 36 HOPS COURT, TAYFEN ROAD, BURY ST. EDMUNDS
            "10009749005",  # BLUE DOORS FARM, COWLINGE, NEWMARKET
            "10009752038",  # MOAT FARM, FARLEY GREEN, NEWMARKET
            "10095885133",  # THE GARDEN FLAT 12 THE AVENUE, NEWMARKET
            "100091370064",  # PEGASUS STABLES SNAILWELL ROAD, NEWMARKET
            "10009750003",  # LEECHMOOR COTTAGE, WEST STOW, BURY ST. EDMUNDS
            "200001366935",  # CUPOLA FARM, UNDLEY, LAKENHEATH, BRANDON
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "CB8 7DJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warning checked and no correction required:
        # WARNING: Polling station The Beeches (19036) is in East Cambridgeshire District Council (ECA)

        # postcode correction and more accurate point for:
        # East Town Park Visitor Centre, Coupals Road, Haverhill, CB9 9QF
        if record.polling_place_id == "19524":
            record = record._replace(polling_place_easting="568610")
            record = record._replace(polling_place_northing="244831")

        return super().station_record_to_dict(record)
