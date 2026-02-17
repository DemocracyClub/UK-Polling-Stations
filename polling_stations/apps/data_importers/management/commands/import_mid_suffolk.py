from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = "2026-05-07/2026-03-24T10:10:12.205290/MSU_Districts_UTF8.tsv"
    stations_name = "2026-05-07/2026-03-24T10:10:12.205290/MSU_stations.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if (
            record.uprn
            in [
                "10095543316",  # PLOT 5 AT TWO OAKS BROCKFORD ROAD, MENDLESHAM
                "10094151033",  # 4 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS, IP31 3UH
                "10094151030",  # 10 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS, IP31 3UH
                "200003806873",  # BADLEY COTTAGE, LITTLE LONDON, COMBS, STOWMARKET, IP14 2ET
                "200003810799",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET, IP14 6EP
                "10095541644",  # DOVEDALE, BROCKFORD ROAD, MENDLESHAM, STOWMARKET, IP14 5SG
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "IP14 6ET",
            "IP14 5LN",
            "IP14 5PE",
            "IP14 1LU",
            # looks wrong
            "IP14 3BS",
            "IP31 3FL",
        ]:
            return None

        return super().address_record_to_dict(record)
