from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2024-05-02/2024-02-19T09:14:43.265455/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-19T09:14:43.265455/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Hale Methodist Church, 119 Hale Road, Hale WA15 9QH
        if record.polling_place_id == "6090":
            record = record._replace(polling_place_postcode="WA15 9HL")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070405338",  # 183A CROSS STREET, SALE
        ]:
            return None

        if record.addressline6 in [
            # split
            "M33 3GG",
            "M33 2BT",
            "WA14 4AN",
            "M33 5GN",
            # confusing
            "M31 4SU",
            "M31 4ST",
        ]:
            return None

        return super().address_record_to_dict(record)
