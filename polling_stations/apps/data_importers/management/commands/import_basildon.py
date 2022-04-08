from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = "2022-05-05/2022-04-08T13:03:58.514518/Basildon Council - Democracy_Club__05May2022.CSV"
    stations_name = "2022-05-05/2022-04-08T13:03:58.514518/Basildon Council - Democracy_Club__05May2022.CSV"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090682049",  # FERNDALE, TYE COMMON ROAD, BILLERICAY
            "100090239089",  # FLAT 1, ST. DAVIDS COURT, LONDON ROAD, BASILDON
            "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
            "10013352273",  # 17 CHURCH ROAD, LAINDON, BASILDON
        ]:
            return None

        if record.addressline6 in [
            "SS15 5DS",
            "SS15 5GX",
            "CM11 2RU",
            "SS15 6PF",
            "CM11 2JX",
            "SS16 6PH",
            "SS12 0AU",
            "CM11 2AD",
            "SS15 5NZ",
            "SS15 5NS",
        ]:
            return None

        return super().address_record_to_dict(record)
