from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAI"
    addresses_name = (
        "2026-05-07/2026-02-24T11:22:45.059332/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-24T11:22:45.059332/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091213142",  # MAYBURY, BORWICK LANE, WICKFORD
                "100091589698",  # ST. NICHOLAS SCHOOL HOUSE, LEINSTER ROAD, BASILDON, SS15 5NS
                "100091432152",  # THE GRANARY, GREENS FARM LANE, BILLERICAY, CM11 2NY
                "100091212751",  # PROBATION OFFICE, 1 FELMORES, BASILDON
                "100090239089",  # 17 CHURCH ROAD, LAINDON, BASILDON
                "100090273531",  # 23 GREENS FARM LANE, BILLERICAY
                "10090682049",  # CEDAR COTTAGE, LOWER DUNTON ROAD, BULPHAN, UPMINSTER
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "SS14 3QQ",
            "CM11 2AD",
            "SS15 6PF",
            "SS12 0AU",
            "CM11 2RU",
            "CM11 2JX",
            "SS15 5NZ",
            "SS15 5GX",
            "CM11 2LH",
            # suspect
            "SS13 3RL",
            "CM11 2XF",
        ]:
            return None

        return super().address_record_to_dict(record)
