from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIF"
    addresses_name = "2024-07-04/2024-06-24T14:06:58.680451/LIF_combined.tsv"
    stations_name = "2024-07-04/2024-06-24T14:06:58.680451/LIF_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100031701504",  # MILL DAM HOUSE, MILL LANE, ALDRIDGE, WALSALL
                "10002767279",  # 4 WISSAGE ROAD, LICHFIELD
                "10002767278",  # 2 WISSAGE ROAD, LICHFIELD
                "100032225708",  # THE COURTYARD, LICHFIELD ROAD, PIPEHILL, LICHFIELD
                "200001160102",  # 86 HIGH STREET, CHASETOWN, BURNTWOOD
                "10013216680",  # MANAGERS ACCOMMODATION TOBY CARVERY BIRMINGHAM ROAD, SHENSTONE WOODEND, LICHFIELD
            ]
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warning was checked nad no correction is needed
        # Polling station Cannock Wood & Gentleshaw Village Hall (9029) is in Cannock Chase District Council (CAN)

        # Holy Cross, Community Meeting Room, Holy Cross Church, WS14 9BA
        if record.polling_place_id == "9005":
            record = record._replace(
                polling_place_easting=411921, polling_place_northing=308789
            )

        # Holy Cross Parish Hall, Holy Cross Parish Hall, Chapel Lane, Lichfield, WS14 9BA
        if record.polling_place_id == "9001":
            record = record._replace(
                polling_place_easting=411908, polling_place_northing=308797
            )

        return super().station_record_to_dict(record)
