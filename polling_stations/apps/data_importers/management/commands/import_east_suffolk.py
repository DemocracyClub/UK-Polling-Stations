from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2024-07-04/2024-06-03T18:14:32.218707/East Suffolk Council - Democracy Club - Polling Districts 4 July 2024.csv"
    stations_name = "2024-07-04/2024-06-03T18:14:32.218707/East Suffolk Council - Democracy Club - Polling Stations 4 July 2024.csv"
    elections = ["2024-07-04"]
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
            # splits
            "NR34 7PU",
            "NR35 1BZ",
            # suspect
            "NR34 8ET",
        ]:
            return None

        return super().address_record_to_dict(record)
