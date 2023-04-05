from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2023-05-04/2023-03-27T11:54:03.935496/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-27T11:54:03.935496/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310084857",  # FLAT 2, 69 NORTHUMBERLAND AVENUE, READING
            "310084859",  # FLAT 4, 69 NORTHUMBERLAND AVENUE, READING
            "310084858",  # FLAT 3, 69 NORTHUMBERLAND AVENUE, READING
            "310064645",  # 1 STAR ROAD, CAVERSHAM, READING
            "310047121",  # BEECH HOUSE HOTEL, 60 BATH ROAD, READING
            "310057403",  # 66 ALEXANDRA ROAD, READING
            "310008722",  # 64 ALEXANDRA ROAD, READING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RG30 3NB",
            "RG30 4RX",
            "RG4 8ES",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Reading Central Library, Abbey Square, Reading, RG1 3BG
        if record.polling_place_id == "4313":
            record = record._replace(polling_place_postcode="RG1 3BQ")

        # Park Lounge, Windsor Hall, University of Reading, Upper Redlands Road, Reading, RG1 5JL
        if record.polling_place_id == "4455":
            record = record._replace(polling_place_postcode="RG6 6HW")

        return super().station_record_to_dict(record)
