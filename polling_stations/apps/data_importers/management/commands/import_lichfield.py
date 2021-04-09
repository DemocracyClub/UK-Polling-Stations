from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIF"
    addresses_name = (
        "2021-03-24T10:59:01.635563/Lichfield Democracy_Club__06May2021.tsv"
    )
    stations_name = "2021-03-24T10:59:01.635563/Lichfield Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Guildroom, Guildhall, Bore Street, Lichfield
        if record.polling_place_id == "5596":
            record = record._replace(polling_place_postcode="WS13 6LU")

        # Mobile Polling Station, Staffs University West Car Park, Monks Close, Lichfield
        if record.polling_place_id == "5583":
            record = record._replace(
                polling_place_easting=411530, polling_place_northing=309223
            )

        # Holy Cross, Community Meeting Room, Holy Cross Church
        if record.polling_place_id == "5595":
            record = record._replace(
                polling_place_easting=411921, polling_place_northing=308789
            )

        # Holy Cross Parish Hall
        if record.polling_place_id == "5591":
            record = record._replace(
                polling_place_easting=411908, polling_place_northing=308797
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002775637",  # HORSEY LANE LODGE, HORSEY LANE, RUGELEY
            "100031701504",  # MILL DAM HOUSE, MILL LANE, ALDRIDGE, WALSALL
            "100031713231",  # THE GRANARY MILL GREEN FARM MILL LANE, ALDRIDGE, WALSALL
            "10002767279",  # 4 WISSAGE ROAD, LICHFIELD
            "10002767278",  # 2 WISSAGE ROAD, LICHFIELD
            "100031692345",  # MILL ACRES HOUSE, DAISY LANE, ALREWAS, BURTON-ON-TRENT
        ]:
            return None

        if record.addressline6 in ["B78 3AU", "WS7 0HZ"]:
            return None

        return super().address_record_to_dict(record)
