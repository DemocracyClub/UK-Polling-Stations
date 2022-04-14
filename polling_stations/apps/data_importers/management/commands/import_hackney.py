from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter

STATION_UPRN_MAP = {
    "HSUB": "100021024344",
    "HNBC": "100021032115",
    "HNHD": "100021040719",
    "HSMA": "100021047828",
    "HNHB": "100021052744",
    "HSPB": "100021053405",
    "HNFA": "100021055040",
    "HNGA": "100021055417",
    "HNIC": "100021056262",
    "HSTB": "100021061125",
    "HSNA": "100021063575",
    "HNJC": "100021066760",
    "HNDB": "100021075143",
    "HNGB": "100021075904",
    "HNBE": "100021078552",
    "HSUC": "100022930896",
    "HSNC": "100023001800",
    "HSNB": "100023001818",
    "HNID": "100023001853",
    "HNEC": "100023007813",
    "HNKA": "100023015443",
    "HNPD": "100023016044",
    "HNKB": "100023016243",
    "HSQB": "100023016926",
    "HSRC": "100023020528",
    "HSIE": "100023020798",
    "HSIF": "100023020798",
    "HSMB": "100023022522",
    "HSSD": "100023024918",
    "HSUA": "100023135347",
    "HSTA": "100023136416",
    "HNAB": "100023156099",
    "HNEA": "100023157700",
    "HNEB": "100023158064",
    "HNBB": "100023159139",
    "HNHA": "100023159605",
    "HNGE": "100023160106",
    "HNAA": "100023184376",
    "HNCC": "100023184497",
    "HSND": "100023546618",
    "HNIB": "100023547501",
    "HNFB": "100023548164",
    "HNFC": "100023647821",
    "HNED": "100023648489",
    "HSLD": "100023649818",
    "HNBD": "100023649898",
    "HSTD": "100023651116",
    "HNHC": "10008235413",
    "HNKC": "10008240149",
    "HSOA": "10008241541",
    "HNGD": "10008242273",
    "HSRA": "10008244238",
    "HNIA": "10008255003",
    "HNFD": "10008288053",
    "HSTC": "10008288169",
    "HSRD": "10008290931",
    "HSOB": "10008291241",
    "HSOC": "10008292317",
    "HNJB": "10008295888",
    "HNDC": "10008305735",
    "HNDD": "10008305735",
    "HNGC": "10008307512",
    "HSSA": "10008307654",
    "HSQD": "10008307752",
    "HSLC": "10008307832",
    "HSMC": "10008307881",
    "HSMD": "10008307922",
    "HNCA": "10008308073",
    "HSQC": "10008308079",
    "HSQE": "10008308090",
    "HNBA": "10008308111",
    "HSPA": "10008308112",
    "HSLE": "10008308117",
    "HNJA": "10008309534",
    "HNAC": "10008328988",
    "HSQA": "10008330088",
    "HSLA": "10008336791",
    "HNDA": "10008338319",
    "HSLB": "10008342143",
    "HSRB": "10008342233",
    "HNCB": "10008348541",
    "HSSB": "200001902506",
    "HSSC": "200001902506",
    "HSPC": "200001906528",
}


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = "2022-05-05/2022-03-23T17:30:06.543100/Democracy_Club__05May2022-HackneyCouncilPollingStations.CSV"
    stations_name = "2022-05-05/2022-03-23T17:30:06.543100/Democracy_Club__05May2022-HackneyCouncilPollingStations.CSV"
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        record = record._replace(
            polling_place_uprn=STATION_UPRN_MAP[record.polling_place_district_reference]
        )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021050062",  # BASEMENT AND GROUND FLOOR 100 LOWER CLAPTON ROAD, HACKNEY, LONDON
            "10008340028",  # FLAT E, 112 KINGSLAND ROAD, LONDON
            "10008300957",  # 85 CASTLEWOOD ROAD, HACKNEY, LONDON
            "200001073528",  # POTTERY HOUSE, ELRINGTON ROAD, LONDON
            "10008233474",
            "10008342758",
            "10008354539",
            "100021076655",
            "10008340573",
            "100021032861",
        ]:
            return None

        if record.addressline6 in [
            "N1 6RH",
            "E20 3AZ",
            "E8 2NS",
            "N4 2ZB",
            "N4 2LD",
            "N4 2WQ",
            "E2 8FZ",
            "N16 0SD",
            "E5 9AP",
            "N16 0RT",
            "EC2A 2FJ",
        ]:
            return None

        return super().address_record_to_dict(record)
