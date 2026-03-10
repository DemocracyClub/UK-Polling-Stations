from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAL"
    addresses_name = "2026-05-07/2026-03-10T13:38:01.597846/Halton Borough Council Democracy_Club__07May2026.tsv"
    stations_name = "2026-05-07/2026-03-10T13:38:01.597846/Halton Borough Council Democracy_Club__07May2026.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        name = record.polling_place_name.replace("`", "'")
        record = record._replace(polling_place_name=name)

        # point correction for: Holy Trinity Church Trinity Street Runcorn WA7 1BJ
        if record.polling_place_id == "6541":
            record = record._replace(polling_place_easting="351595")
            record = record._replace(polling_place_northing="383048")

        # User issue #572
        # point correction for: St Michael's Catholic Church, St Michael's Road, Widnes, WA8 8TF
        if record.polling_place_id == "6583":
            record = record._replace(polling_place_easting="349445")
            record = record._replace(polling_place_northing="385338")

        # point correction for: St Johns Church, 134 Greenway Road, Widnes, WA8 6HA
        if record.polling_place_id == "6489":
            record = record._replace(polling_place_easting="351638")
            record = record._replace(polling_place_northing="386586")

        # point correction for: Mobile Polling Station Galway Ave. Widnes
        if record.polling_place_id == "6532":
            record = record._replace(polling_place_easting="350203")
            record = record._replace(polling_place_northing="387149")

        # point correction for: Beechwood Community Centre, Beechwood Avenue, Runcorn, WA7 3HB
        if record.polling_place_id == "6522":
            record = record._replace(polling_place_easting="353075")
            record = record._replace(polling_place_northing="380317")

        # point correction for: Prescot Road Changing Rooms, Hough Green Road, Widnes, WA8 7PD
        if record.polling_place_id == "6678":
            record = record._replace(polling_place_easting="349493")
            record = record._replace(polling_place_northing="387054")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "WA8 7TB",
            "WA7 4SX",
            "WA7 1BH",
            "WA8 7TF",
            "WA8 8PZ",
            "WA7 4BS",
        ]:
            return None

        return super().address_record_to_dict(record)
