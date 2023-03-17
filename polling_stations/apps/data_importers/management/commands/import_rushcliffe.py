from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUS"
    addresses_name = "2023-05-04/2023-03-17T17:04:03.550393/Democracy_Club__04May2023_Rushcliffe BC.CSV"
    stations_name = "2023-05-04/2023-03-17T17:04:03.550393/Democracy_Club__04May2023_Rushcliffe BC.CSV"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Bingham Methodist Centre, Union Street, Bingham, Nottingham
        if record.polling_place_id == "6000":
            record = record._replace(polling_place_easting="470360")

        # Edwalton Church Hall, Vicarage Green, Edwalton
        if record.polling_place_id == "5924":
            record = record._replace(polling_place_easting="459770")

        # West Bridgford Baptist Church, Melton Road, West Bridgford
        if record.polling_place_id == "5846":
            record = record._replace(polling_place_easting="458380")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "NG2 5JT",
            "NG13 8GP",
        ]:
            return None

        return super().address_record_to_dict(record)
