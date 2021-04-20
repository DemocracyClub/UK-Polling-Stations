from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TWH"
    addresses_name = "2021-04-19T16:17:20.397298/Tower_Hamlets_deduped.csv"
    stations_name = "2021-04-19T16:17:20.397298/Tower_Hamlets_deduped.csv"
    elections = ["2021-05-06"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "6198433":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "E2 9DG"
            return rec

        # 11 BILLSON STREET, LONDON
        if uprn in [
            "6728119",  # 11 BILLSON STREET, LONDON
            "6146893",  # 80B BRUCE ROAD, LONDON
            "6703128",  # FLAT 3, BUSTLE COURT, 11 CRINOLINE MEWS, LONDON
        ]:
            return None
        if record.addressline6 in ["E14 6EL", "E1 0BH"]:
            return None

        return super().address_record_to_dict(record)
