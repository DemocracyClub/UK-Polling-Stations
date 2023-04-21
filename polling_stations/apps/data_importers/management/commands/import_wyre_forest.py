from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = (
        "2023-05-04/2023-04-21T13:58:09.119512/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T13:58:09.119512/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003382058",  # THE PATCH, LEIGHT LANE, RIBBESFORD, BEWDLEY
            "100120755484",  # CONEY GREEN FARM, RIBBESFORD ROAD, STOURPORT-ON-SEVERN
            "100120755483",  # CONEY GREEN COTTAGE, RIBBESFORD ROAD, STOURPORT-ON-SEVERN
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DY10 2QD",
            "DY10 3TF",
            "DY12 2TN",
            "DY10 1LS",
            "DY11 5QT",
            "DY12 2LF",
            "DY10 3HJ",
        ]:
            return None

        return super().address_record_to_dict(record)
