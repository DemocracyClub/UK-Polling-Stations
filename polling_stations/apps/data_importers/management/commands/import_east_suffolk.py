from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2024-05-02/2024-03-11T11:06:27.248527/Democracy Club - Polling Districts - East Suffolk - 2 May 2024.csv"
    stations_name = "2024-05-02/2024-03-11T11:06:27.248527/Democracy Club - Polling Stations - East Suffolk - 2 May 2024.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091154936",  # 6 THE PIGHTLE, NORTH COVE, BECCLES
            "100091487163",  # ISLAND COTTAGE, THE STREET, HACHESTON, WOODBRIDGE
            "100091638545",  # HEATH COTTAGE, FOXHALL, IPSWICH
        ]:
            return None
        if record.postcode in [
            "NR35 1BZ",  # split
            "NR34 8ET",  # weird
        ]:
            return None

        return super().address_record_to_dict(record)
