from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = (
        "2023-05-04/2023-03-09T12:06:08.847842/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-09T12:06:08.847842/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
            "10013352273",  # 17 CHURCH ROAD, LAINDON, BASILDON
        ]:
            return None

        if record.addressline6 in [
            "SS15 6PF",
            "CM11 2RU",
            "CM11 2AD",
            "SS15 5NZ",
        ]:
            return None

        return super().address_record_to_dict(record)
