from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEC"
    addresses_name = (
        "2026-05-07/2026-03-23T12:19:26.156049/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-23T12:19:26.156049/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Higherland Methodist Church Hall Higherland Newcastle Staffs ST5 2TF
        if record.polling_place_id == "4309":
            record = record._replace(polling_place_easting="384574")
            record = record._replace(polling_place_northing="345703")

        # waiting for council response
        # # add missing location for: Newcastle-under-Lyme Children`s Centre, Cemetery Road, Knutton, Newcastle-under-Lyme, Staffs
        # if record.polling_place_id == "4468":
        #     record = record._replace(polling_place_postcode="", polling_place_easting="", polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200002872601",  # 125A LIVERPOOL ROAD, NEWCASTLE
                "200004609337",  # 290 AUDLEY ROAD, NEWCASTLE
                "10024256416",  # OAK HOUSE, SECOND AVENUE, NEWCASTLE
                "200004616745",  # WILLOUGHBRIDGE FARM, WILLOUGHBRIDGE, MARKET DRAYTON
                "200004610893",  # 147 WILLOUGHBRIDGE, MARKET DRAYTON
                "10094842027",  # MANAGERS ACCOMODATION THE COTTON MILL LIVERPOOL ROAD, NEWCASTLE UNDER LYME
                "200004608253",  # SILVERDALE WORKING MENS CLUB, 98 HIGH STREET, SILVERDALE, NEWCASTLE
                "200004616223",  # YEW TREE COTTAGE, HILL CHORLTON, NEWCASTLE
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "ST5 8QG",
            # suspect
            "ST5 6BS",
            "ST5 6BU",
            "ST7 3PX",
            "ST5 4DH",
            "ST7 1XH",
        ]:
            return None

        return super().address_record_to_dict(record)
