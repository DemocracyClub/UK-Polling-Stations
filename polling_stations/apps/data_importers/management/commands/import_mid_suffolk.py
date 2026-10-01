from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = (
        "2026-11-12/2026-10-01T10:44:42.468120/Bosmere - Pollingdistricts.csv"
    )
    stations_name = (
        "2026-11-12/2026-10-01T10:44:42.468120/Bosmere - Pollingstations.csv"
    )
    elections = ["2026-11-12"]
    csv_encoding = "utf-16le"

    # maintaining some tweaks as comments through by-election
    def address_record_to_dict(self, record):
        if record.uprn in [
            # "10095543316",  # PLOT 5 AT TWO OAKS BROCKFORD ROAD, MENDLESHAM
            # "10094151033",  # 4 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS, IP31 3UH
            # "10094151030",  # 10 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS, IP31 3UH
            # "200003806873",  # BADLEY COTTAGE, LITTLE LONDON, COMBS, STOWMARKET, IP14 2ET
            # "200003810799",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET, IP14 6EP
            # "10095541644",  # DOVEDALE, BROCKFORD ROAD, MENDLESHAM, STOWMARKET, IP14 5SG
            "10096503787",  # ANNEXE AT HOLLY FARM DEADMANS LANE, BATTISFORD
        ]:
            return None

        if (
            record.postcode
            in [
                # looks wrong
                # "IP14 3BS",
                # "IP31 3FL",
            ]
        ):
            return None

        return super().address_record_to_dict(record)
