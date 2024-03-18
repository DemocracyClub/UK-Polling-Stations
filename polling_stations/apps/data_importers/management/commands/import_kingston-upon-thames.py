from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = (
        "2024-05-02/2024-03-05T11:00:16.877806/RBK Polling Districts List.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T11:00:16.877806/RBK Polling Stations List.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "latin-1"

    # Following warnings checked and no correction needed
    # WARNING: Polling station Oak Hall, Maple Lodge (MPC) is in London Borough of Sutton (STN)

    def station_record_to_dict(self, record):
        # fix from council:
        # old address: St. John's Parish Hall, Grove Lane, Kingston upon Thames KT1 2SU
        # new address: St. John's Parish Hall, Grove Lane, Kingston upon Thames KT1 2ST
        if record.stationcode == "KTC":
            record = record._replace(postcode="KT1 2ST")

        # fix from council:
        # old address: Catholic Church of St. Pius X, The Triangle, Kingston Upon Thames, Surrey KT1 3SB
        # new address: Temporary station side of St Pius X Catholic Church, The Triangle, Kingston Upon Thames, Surrey KT1 3RU
        if record.stationcode == "CVD":
            record = record._replace(
                placename="Temporary station side of St Pius X Catholic Church",
                postcode="KT1 3RU",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "128039658",  # FLAT 59 CAMBRIDGE ROAD, KINGSTON UPON THAMES
            "128039914",  # ANNEXE 58 GLOUCESTER ROAD, KINGSTON UPON THAMES
            "128038772",  # 58A CLIFTON ROAD, KINGSTON UPON THAMES
            "128038771",  # 58 CLIFTON ROAD, KINGSTON UPON THAMES
            "128040253",  # 1 CAMBRIDGE GARDENS, KINGSTON UPON THAMES
            "128014595",  # 28 PENRHYN ROAD, KINGSTON UPON THAMES
            "128043396",  # SILVERWOOD HOUSE, GEORGE ROAD, KINGSTON UPON THAMES
            "128007539",  # MAXGATE, GEORGE ROAD, KINGSTON UPON THAMES
        ]:
            return None

        return super().address_record_to_dict(record)
