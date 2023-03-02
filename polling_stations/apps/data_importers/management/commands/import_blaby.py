from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BLA"
    addresses_name = (
        "2023-05-04/2023-03-02T14:37:46.931832/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T14:37:46.931832/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001230049",  # MARRIOTT HOTEL, SMITH WAY, GROVE PARK, ENDERBY, LEICESTER
            "100030407216",  # 2 WARWICK ROAD, WHETSTONE, LEICESTER
            "100030407215",  # 4 WARWICK ROAD, WHETSTONE, LEICESTER
            "10001236400",  # PITCH 11 LAND TO SOUTH EAST OF WHITE GATE STABLES HINCKLEY ROAD, SAPCOTE
            "10001225839",  # GREEN ACRES, HOSPITAL LANE, BLABY, LEICESTER
        ]:
            return None

        if record.addressline6 in [
            "LE19 1SJ",  # MANAGERS, ASSISTANT FLATS
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Millfield Community Nursery, Millfield L.E.A.D. Academy, Hat Road, Braunstone Town, Leicester
        if record.polling_place_id == "3878":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        # Stafford Leys Community Centre - Station 2, Stafford Leys Primary School, Stafford Leys
        if record.polling_place_id == "3849":
            record = record._replace(
                polling_place_easting="452960", polling_place_northing="302987"
            )

        # Springwell, Whetstone Baptist Church, Dog and Gun Lane, Whetstone, Leicester
        if record.polling_place_id == "3923":
            record = record._replace(polling_place_postcode="LE8 6LJ")

        return super().station_record_to_dict(record)
