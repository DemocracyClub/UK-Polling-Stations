from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = (
        "2026-05-07/2026-02-03T16:42:33.559509/CEREDIGION - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-02-03T16:42:33.559509/CEREDIGION - Polling Stations.csv"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        """
        The file we received from Ceredigion this time (2026)
        has every address in it 4 times.
        Mostly they are just exact duplicates. However we have around 6,000
        cases where the same UPRN is assigned to 2 different station codes.
        However in all these cases, one of the station codes exists
        and the other one doesn't.
        If we exclude all of these UPRNs, we end up with some stations that
        have no addresses assigned to them at all.
        If we drop any row with a station code that doesn't exist in the
        stations file, that essentially says
        "if this UPRN is assigned to >1 station, assume the one that exists"
        and basically everything imports.
        """
        bad_codes = [
            "1-1070/1071/1072",
            "66-1087",
            "69-1090",
            "55-1073",
            "11-1013",
            "38-1063",
            "76-1063",
            "12-1030/1031",
            "37-1049/1062",
            "68-1089",
        ]
        if record.stationcode in bad_codes:
            return None

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
