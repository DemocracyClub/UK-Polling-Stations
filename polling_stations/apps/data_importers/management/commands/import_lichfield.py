from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIF"
    addresses_name = (
        "2023-05-04/2023-04-19T15:20:06.691978/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-19T15:20:06.691978/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002775637",  # HORSEY LANE LODGE, HORSEY LANE, RUGELEY
            "100031701504",  # MILL DAM HOUSE, MILL LANE, ALDRIDGE, WALSALL
            "10002767279",  # 4 WISSAGE ROAD, LICHFIELD
            "10002767278",  # 2 WISSAGE ROAD, LICHFIELD
            "100032225708",  # THE COURTYARD, LICHFIELD ROAD, PIPEHILL, LICHFIELD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Guildroom, Guildhall, Bore Street, Lichfield, WS13 6LX
        if record.polling_place_id == "6502":
            record = record._replace(polling_place_postcode="WS13 6LU")

        # Holy Cross, Community Meeting Room, Holy Cross Church, WS14 9BA
        if record.polling_place_id == "6758":
            record = record._replace(
                polling_place_easting=411921, polling_place_northing=308789
            )

        # Holy Cross Parish Hall, Holy Cross Parish Hall, Chapel Lane, Lichfield, WS14 9BA
        if record.polling_place_id == "6754":
            record = record._replace(
                polling_place_easting=411908, polling_place_northing=308797
            )

        return super().station_record_to_dict(record)
