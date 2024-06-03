from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = "2024-07-04/2024-06-10T11:19:58.273691/ktt-districts-combined.csv"
    stations_name = "2024-07-04/2024-06-10T11:19:58.273691/ktt-stations-combined.csv"
    elections = ["2024-07-04"]

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
        if record.postcode in [
            "KT2 7DA",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
