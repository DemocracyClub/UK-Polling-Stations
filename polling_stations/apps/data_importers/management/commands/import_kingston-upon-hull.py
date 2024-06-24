from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = (
        "2024-07-04/2024-06-24T11:06:48.123709/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-24T11:06:48.123709/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "21133711",  # FLAT OVER 19 18-19 WITHAM, KINGSTON UPON HULL
            "21133712",  # FLAT OVER 121 121-127 WITHAM, KINGSTON UPON HULL
            "10093952515",  # 321A BEVERLEY ROAD, HULL
            "10093952516",  # 323A BEVERLEY ROAD, HULL
            "21051039",  # 86 HOWDALE ROAD, HULL
        ]:
            return None

        if record.addressline6 in [
            # split
            "HU5 2RH",
            "HU5 3LT",
            "HU5 5NT",
        ]:
            return None

        return super().address_record_to_dict(record)
