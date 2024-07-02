from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = (
        "2024-07-04/2024-06-14T14:22:31.403452/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T14:22:31.403452/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
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
            "49061980",  # Y DDOL LLAWEN, CWMRHEIDOL, ABERYSTWYTH
        ]:
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

        # Remove stations from the PEM council
        if record.stationcode in [
            "100-2025",
            "00-2025",
            "101-2026",
            "102-2027",
            "77-2001",
            "78-2002",
            "79-2003",
            "80-2004",
            "81-2005",
            "82-2006",
            "83-2007",
            "83-2008",
            "84-2009",
            "85-2010",
            "86-2011",
            "87-2012",
            "88-2013",
            "89-2014",
            "90-2015",
            "91-2016",
            "92-2017",
            "93-2018",
            "94-2019",
            "95-2020",
            "96-2021",
            "97-2022",
            "98-2023",
            "99-2024",
        ]:
            return None
        # bug report #693: removes potentially wrong postcode for:
        # NEUADD EGLWYS LLANARTH CHURCH HALL, LLANARTH, SA47 0NP
        if record.stationcode == "49-1058":
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
