from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = (
        "2023-05-04/2023-04-05T10:06:21.347042/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-05T10:06:21.347042/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091600419",  # THE GRANGE, GRANGE ROAD, BENFLEET
            "200000992512",  # THE BRAMBLES SHIPWRIGHTS CLOSE, SOUTH BENFLEET, BENFLEET
            "100091228650",  # MANOR HOUSE, SHIPWRIGHTS CLOSE, BENFLEET
        ]:
            return None

        if record.addressline6 in [
            # split
            "SS8 8HN",
            "SS8 9SL",
        ]:
            return None

        return super().address_record_to_dict(record)
