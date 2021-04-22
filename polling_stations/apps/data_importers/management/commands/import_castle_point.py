from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = "2021-04-12T09:02:05.837447/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-12T09:02:05.837447/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100090361765",  # 35 LONDON ROAD, BENFLEET
            "100091600419",  # THE GRANGE, GRANGE ROAD, BENFLEET
            "10004940533",  # CARAVAN 9E2 THORNEY BAY CARAVAN PARK THORNEY BAY ROAD, CANVEY ISLAND
            "10004940535",  # CARAVAN 9I3 THORNEY BAY CARAVAN PARK THORNEY BAY ROAD, CANVEY ISLAND
            "10004940532",  # CARAVAN 8A1 THORNEY BAY CARAVAN PARK THORNEY BAY ROAD, CANVEY ISLAND
            "10004940527",  # CARAVAN 8F5 THORNEY BAY CARAVAN PARK THORNEY BAY ROAD, CANVEY ISLAND
            "10004934986",  # 5 STATION ROAD, CANVEY ISLAND
            "100090382770",  # 62 WAARDEN ROAD, CANVEY ISLAND
        ]:
            return None

        if record.addressline6 in [
            "SS8 9JH",
            "SS8 8HN",
            "SS8 7RN",
            "SS8 9SL",
            "SS7 3PJ",
        ]:
            return None

        return super().address_record_to_dict(record)
