from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIV"
    addresses_name = (
        "2024-07-04/2024-06-03T17:22:44.406254/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-03T17:22:44.406254/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "38159023",  # 304 WALTON LANE, LIVERPOOL
            "38159026",  # 308 WALTON LANE, LIVERPOOL
            "38159021",  # 302 WALTON LANE, LIVERPOOL
            "38140298",  # 124 SMITHDOWN ROAD, LIVERPOOL
            "38117786",  # 28 PICTON ROAD, WAVERTREE, LIVERPOOL
            "38277973",  # WALTON HALL PARK LODGE, WALTON HALL AVENUE, LIVERPOOL
            "38039505",  # AINTREE LODGE, CROXTETH PARK, LIVERPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L3 6LH",
            "L13 4AU",
            "L11 4TD",
            # suspect
            "L16 0JW",  # CHILDWALL ABBEY ROAD, LIVERPOOL
            "L9 9EN",  # LONGMOOR LANE, LIVERPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # bugreport #648
        # postcode correction for: St.Mary`s Church Parish Hall, St Mary`s Road, Liverpool, L19 0PW
        if record.polling_place_id == "11514":
            record = record._replace(polling_place_postcode="L19 0NE")

        return super().station_record_to_dict(record)
