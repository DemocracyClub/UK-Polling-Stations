from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEC"
    addresses_name = (
        "2025-05-01/2025-03-11T11:45:15.531010/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-11T11:45:15.531010/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Higherland Methodist Church Hall Higherland Newcastle Staffs ST5 2TF
        if record.polling_place_id == "4070":
            record = record._replace(polling_place_easting="384574")
            record = record._replace(polling_place_northing="345703")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002872601",  # 125A LIVERPOOL ROAD, NEWCASTLE
            "100031723127",  # 7 DEANS LANE, NEWCASTLE
            "100031723126",  # 6 DEANS LANE, NEWCASTLE
            "100031723129",  # STARBOROUGH HOUSE, DEANS LANE, NEWCASTLE
            "100031723128",  # 8 DEANS LANE, NEWCASTLE
            "200004609337",  # 290 AUDLEY ROAD, NEWCASTLE
        ]:
            return None

        if record.addressline6 in [
            # split
            "ST5 8QG",
            # suspect
            "ST5 6BS",
        ]:
            return None

        return super().address_record_to_dict(record)
