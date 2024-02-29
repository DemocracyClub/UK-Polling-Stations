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
