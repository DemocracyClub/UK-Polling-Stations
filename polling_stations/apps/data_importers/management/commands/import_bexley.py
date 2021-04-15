from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BEX"
    addresses_name = "2021-04-15T09:27:46.954886/Democracy_Club__06May2021 (1).tsv"
    stations_name = "2021-04-15T09:27:46.954886/Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Point supplied for Footscray Baptist Church is miles off
        if record.polling_place_id == "2458":
            record = record._replace(
                polling_place_easting="547145", polling_place_northing="171147"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020267460",  # 69 CUMBERLAND AVENUE, WELLING
            "10023303792",  # FLAT 3, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303790",  # FLAT 1, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303794",  # FLAT 5, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303793",  # FLAT 4, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303796",  # FLAT 7, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303791",  # FLAT 2, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
            "10023303795",  # FLAT 6, LAWRENCE COURT, 120 MAIN ROAD, SIDCUP
        ]:
            return None

        if record.addressline6 in ["DA15 7DU", "DA7 6BS"]:
            return None

        return super().address_record_to_dict(record)
