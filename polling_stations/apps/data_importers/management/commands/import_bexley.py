from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BEX"
    addresses_name = "2021-11-22T15:59:25.137997/Democracy_Club__02December2021.tsv"
    stations_name = "2021-11-22T15:59:25.137997/Democracy_Club__02December2021.tsv"
    elections = ["2021-12-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Point supplied for Footscray Baptist Church is miles off
        if record.polling_place_id == "2812":
            record = record._replace(
                polling_place_easting="547145", polling_place_northing="171147"
            )
        return super().station_record_to_dict(record)
