from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIF"
    addresses_name = (
        "2024-05-02/2024-04-12T15:39:26.541706/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T15:39:26.541706/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031701504",  # MILL DAM HOUSE, MILL LANE, ALDRIDGE, WALSALL
            "10002767279",  # 4 WISSAGE ROAD, LICHFIELD
            "10002767278",  # 2 WISSAGE ROAD, LICHFIELD
            "100032225708",  # THE COURTYARD, LICHFIELD ROAD, PIPEHILL, LICHFIELD
            "200001160102",  # 86 HIGH STREET, CHASETOWN, BURNTWOOD
            "10013216680",  # MANAGERS ACCOMMODATION TOBY CARVERY BIRMINGHAM ROAD, SHENSTONE WOODEND, LICHFIELD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warning was checked nad no correction is needed
        # Polling station Cannock Wood & Gentleshaw Village Hall (8162) is in Cannock Chase District Council (CAN)

        # Holy Cross, Community Meeting Room, Holy Cross Church, WS14 9BA
        if record.polling_place_id == "7791":
            record = record._replace(
                polling_place_easting=411921, polling_place_northing=308789
            )

        # Holy Cross Parish Hall, Holy Cross Parish Hall, Chapel Lane, Lichfield, WS14 9BA
        if record.polling_place_id == "7787":
            record = record._replace(
                polling_place_easting=411908, polling_place_northing=308797
            )

        return super().station_record_to_dict(record)
