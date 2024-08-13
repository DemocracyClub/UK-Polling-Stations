from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BLA"
    addresses_name = (
        "2024-07-04/2024-05-27T15:58:42.972617/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-27T15:58:42.972617/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10001230049",  # MARRIOTT HOTEL, SMITH WAY, GROVE PARK, ENDERBY, LEICESTER
                "100030407216",  # 2 WARWICK ROAD, WHETSTONE, LEICESTER
                "100030407215",  # 4 WARWICK ROAD, WHETSTONE, LEICESTER
                "10001236400",  # PITCH 11 LAND TO SOUTH EAST OF WHITE GATE STABLES HINCKLEY ROAD, SAPCOTE
                "10001225839",  # GREEN ACRES, HOSPITAL LANE, BLABY, LEICESTER
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "LE19 1SJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warnings checked and no correction needed:
        # WARNING: Polling station Parkland Primary School (4281) is in Oadby & Wigston Borough Council (OAD)
        # WARNING: Polling station Riverside Football Pavilion (4314) is in Leicester City Council (LCE)

        # Millfield Community Nursery, Millfield L.E.A.D. Academy, Hat Road, Braunstone Town, Leicester, LE3 2WF
        if record.polling_place_id == "4379":
            record = record._replace(
                polling_place_easting="455360", polling_place_northing="301508"
            )

        return super().station_record_to_dict(record)
