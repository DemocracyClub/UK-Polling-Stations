from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BLA"
    addresses_name = (
        "2025-05-01/2025-03-10T16:05:45.756880/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T16:05:45.756880/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
        if record.polling_place_id == "4784":
            record = record._replace(
                polling_place_easting="455360", polling_place_northing="301508"
            )

        # The following stations don't have coordinate data in the council data, but they are located at a polling place
        # with the multiple stations, so we can use the coordinates of the other station at the polling place.

        # Whetstone Memorial Hall - Station 2 High Street Whetstone Leicester
        if record.polling_place_id == "4791":
            record = record._replace(
                polling_place_easting="455703", polling_place_northing="297428"
            )
        # Kirby Muxloe Village Hall - Station 2 Station Road Kirby Muxloe
        if record.polling_place_id == "4794":
            record = record._replace(
                polling_place_easting="452030", polling_place_northing="303926"
            )
        return super().station_record_to_dict(record)
