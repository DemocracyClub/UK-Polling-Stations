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

    def station_record_to_dict(self, record):
        # The following are stations amendments for the council:

        # Christ Church C Of E Primary School, Pine Garden, Surbiton
        if record.stationcode == "BRA-K_3":
            record = record._replace(xordinate="519309", yordinate="167339")

        # Old Malden Children's Centre, Lawrence Avenue, New Malden
        if record.stationcode == "OMA-W_46":
            record = record._replace(xordinate="521105", yordinate="166696")

        # Temporary Station - Kings College Sports Ground, Windsor Avenue, New Malden
        if record.stationcode == "GLD-W_22":
            record = record._replace(xordinate="520201.89", yordinate="167894.86")

        # Temporary Station Norbiton Train Station, Coombe Road, Kingston Upon Thames
        if record.stationcode == "RP-CHB":
            record = record._replace(xordinate="519450.08", yordinate="169539.84")

        # St Pius X Catholic Church, The Triangle, The Triangle, Kingston Upon Thames, Surrey
        if record.stationcode == "RP-CVD":
            record = record._replace(placename="St Pius X Catholic Church")
        return super().station_record_to_dict(record)
