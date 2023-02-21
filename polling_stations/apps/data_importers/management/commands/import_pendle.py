from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PEN"
    addresses_name = (
        "2022-05-05/2022-03-07T13:15:49.169874/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-07T13:15:49.169874/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Thomas Street Bowling Pavilion, Percy Street, Nelson BB9 9AY
        if record.polling_place_id == "4317":
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
