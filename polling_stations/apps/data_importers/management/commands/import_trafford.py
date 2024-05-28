from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2024-07-04/2024-05-28T18:53:03.135580/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T18:53:03.135580/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070405338",  # 183A CROSS STREET, SALE
        ]:
            return None

        if record.addressline6 in [
            # split
            "M33 5GN",
            "M33 2BT",
            "M33 3GG",
            "WA14 4AN",
            # confusing
            "M31 4SU",
            "M31 4ST",
            "WA15 8TR",
        ]:
            return None

        return super().address_record_to_dict(record)
