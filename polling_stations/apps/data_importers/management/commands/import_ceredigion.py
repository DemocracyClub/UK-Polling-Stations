from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = "2026-05-07/2026-02-05T14:21:50.846783/CEREDIGION - Democracy Club - Polling Districts_05.03.2026.csv"
    stations_name = "2026-05-07/2026-02-05T14:21:50.846783/CEREDIGION - Democracy Club - Polling Stations_05.03.2026.csv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "49062840",  # TY GWYN, LLANARTH
                "49049138",  # AWEL Y BRYN, RHYDLEWIS, LLANDYSUL
                "49069702",  # TYDDYN MEHERYN, RHYDLEWIS, LLANDYSUL
                "49047840",  # ALMA, TANYGROES, CARDIGAN
                "49040771",  # TROEDYRHIW, BETHANIA, LLANON
                "49065819",  # THE WILLOW, CROSS INN, LLANON
                "49069384",  # TROEDYRHIW CAPELI, CRIBYN, LAMPETER
                "49075931",  # BRYN BARCUD, GORSGOCH, LLANYBYDDER
                "49037718",  # CARTREFLE, MYDROILYN, LAMPETER
                "49062368",  # TY GWALIA, LLWYNYGROES, TREGARON
                "49061701",  # GER Y NANT, CAPEL BANGOR, ABERYSTWYTH
                "49040891",  # TYNGWNDWN, LLANFARIAN, ABERYSTWYTH
                "49065752",  # TY'R IET, CARDIGAN
                "49063434",  # CARDIGAN SAND & GRAVEL CO LTD, CNWC Y SAESON, PENPARC, CARDIGAN
                "49047095",  # CRYNGA MAWR, BLAENANNERCH, CARDIGAN
                "200001099702",  # PLASBRYNIAU, LADY ROAD, BLAENPORTH, CARDIGAN
                "49048192",  # MAESGWYN, GLYNARTHEN, LLANDYSUL
                "49038741",  # TEGLAN, CILIAU AERON, LAMPETER
                "49061980",  # Y DDOL LLAWEN, CWMRHEIDOL, ABERYSTWYTH
            ]
        ):
            return None

        if record.postcode in [
            # split
            "SA44 5UB",
            # suspect
            "SA44 5NQ",
            "SY23 5JP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Remove duplicated stations names
        record = record._replace(placename="")

        return super().station_record_to_dict(record)
