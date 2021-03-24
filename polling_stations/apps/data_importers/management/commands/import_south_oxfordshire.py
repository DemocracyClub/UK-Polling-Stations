from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOX"
    addresses_name = "2021-03-18T11:05:52.448256/UPDATED Democracy_Club__06May2021.TSV"
    stations_name = "2021-03-18T11:05:52.448256/UPDATED Democracy_Club__06May2021.TSV"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100121305054",  # THE OXFORDSHIRE, RYCOTE LANE, MILTON COMMON, THAME
            "100120895687",  # THE OLD PUMP HOUSE, KINGSEY ROAD, THAME
        ]:
            return None

        if record.addressline6 in [
            "OX11 8JW",
            "OX11 9EW",
            "RG9 2HZ",
            "RG9 4PX",
            "OX11 7PT",
            "OX11 6DE",
            "OX10 0FJ",
            "RG8 0BS",
            "OX11 8RE",
            "OX9 2AD",
            "OX11 8AU",
            "OX11 7DT",
            "OX11 6JL",
            "OX11 6ES",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Thame Snooker Club 1a Saint Andrew Court Wellington Street Thame OX9 3WT
        if record.polling_place_id == "11459":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
