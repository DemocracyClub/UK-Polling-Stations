from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PEN"
    addresses_name = (
        "2023-05-04/2023-03-09T12:04:45.963515/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-09T12:04:45.963515/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Thomas Street Bowling Pavilion, Percy Street, Nelson BB9 9AY
        if record.polling_place_id == "4554":
            record = record._replace(
                polling_place_northing=437261,
                polling_place_easting=386085,
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BB9 0RQ",
            "BB9 7YS",
        ]:
            return None

        return super().address_record_to_dict(record)
