from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = "2021-03-16T14:11:49.270209/Democracy_Club__06May2021.csv"
    stations_name = "2021-03-16T14:11:49.270209/Democracy_Club__06May2021.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091587330",  # CEDAR COTTAGE, LOWER DUNTON ROAD, BULPHAN, UPMINSTER
            "10090682049",  # FERNDALE, TYE COMMON ROAD, BILLERICAY
            "100090239089",  # FLAT 1, ST. DAVIDS COURT, LONDON ROAD, BASILDON
            "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
            "10013352273",  # 17 CHURCH ROAD, LAINDON, BASILDON
            "100090273531",  # 23 GREENS FARM LANE, BILLERICAY
        ]:
            return None

        if record.addressline6 in [
            "SS12 0AU",
            "SS15 5GX",
            "CM11 2ER",
            "SS13 2EA",
            "CM11 2JX",
            "CM11 2AD",
            "CM12 9JJ",
            "SS15 6GJ",
            "SS15 6PF",
            "SS13 3EA",
            "CM11 1HH",
            "SS15 5NZ",
            "CM11 2RU",
            "SS16 5PW",
            "SS13 2LG",
            "SS16 6PH",
            "SS12 9LE",
            "SS14 3RZ",
        ]:
            return None

        return super().address_record_to_dict(record)
