from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = (
        "2024-07-04/2024-05-29T11:06:33.058529/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-29T11:06:33.058529/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
            "100090239089",  # 17 CHURCH ROAD, LAINDON, BASILDON
            "100090273531",  # 23 GREENS FARM LANE, BILLERICAY
            "10090682049",  # CEDAR COTTAGE, LOWER DUNTON ROAD, BULPHAN, UPMINSTER
        ]:
            return None

        if record.addressline6 in [
            # split
            "SS15 5GX",
            "CM11 2JX",
            "SS15 6PF",
            "CM11 2RU",
            "SS12 0AU",
            "CM11 2AD",
            "CM11 2LH",
            "SS16 6PH",
            "SS15 5NZ",
            # suspect
            "SS13 3RL",
        ]:
            return None

        return super().address_record_to_dict(record)
