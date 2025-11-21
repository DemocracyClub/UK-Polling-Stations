from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = (
        "2024-05-02/2024-03-26T15:55:08.555130/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-26T15:55:08.555130/Democracy Club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
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
        ]:
            return None

        if record.postcode in [
            # split
            "SA44 5UB",
            "SA43 1PT",
            # suspect
            "SA44 5NQ",
            "SY23 5JP",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        record = record._replace(placename="")
        return super().station_record_to_dict(record)
