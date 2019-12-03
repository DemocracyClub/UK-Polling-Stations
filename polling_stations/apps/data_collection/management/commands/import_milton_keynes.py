from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000042"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019MK.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019MK.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7950":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        if record.polling_place_id == "7890":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        if record.polling_place_id == "7667":  # The Olney Centre
            record = record._replace(polling_place_easting="488859")
            record = record._replace(polling_place_northing="251779")
        if record.polling_place_id == "7915":  # Heronsbrook Meeting Place
            record = record._replace(polling_place_easting="489631")
            record = record._replace(polling_place_northing="235987")
        if record.polling_place_id == "7909":  # Church of The Holy Cross
            record = record._replace(polling_place_easting="482483")
            record = record._replace(polling_place_northing="238427")
        if record.polling_place_id == "7650":  # Portfields Community Centre 2
            record = record._replace(polling_place_easting="486235")
            record = record._replace(polling_place_northing="243915")
        if record.polling_place_id == "7581":  # Oldbrook Community Centre
            record = record._replace(polling_place_easting="485474")
            record = record._replace(polling_place_northing="237785")
        if record.polling_place_id == "7659":  # Lovat Hall Polling Station 2
            record = record._replace(polling_place_easting="487574")
            record = record._replace(polling_place_northing="243582")

        return super().station_record_to_dict(record)
