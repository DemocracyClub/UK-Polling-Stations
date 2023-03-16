from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = "2023-05-04/2023-03-30T13:36:19.020481/ems_exports_combined.tsv"
    stations_name = "2023-05-04/2023-03-30T13:36:19.020481/ems_exports_combined.tsv"
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "200000182939",  # CARAVAN 1 POINTERS PADDOCK SHEARDLEY LANE, DROXFORD
            "200000179695",  # CARAVAN 2 POINTERS PADDOCK SHEARDLEY LANE, DROXFORD
            "10094862207",  # 3 CAMPION ROAD, CURBRIDGE
        ]:
            return None
        if record.addressline6 in [
            # split
            "SO24 9HZ",
            "SO32 1HP",
            "SO32 3PJ",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Upham New Millennium Village Hall (Cttee Room)
        if record.polling_place_id == "10504":
            record = record._replace(polling_place_easting="452220")
            record = record._replace(polling_place_northing="119570")

        return super().station_record_to_dict(record)
