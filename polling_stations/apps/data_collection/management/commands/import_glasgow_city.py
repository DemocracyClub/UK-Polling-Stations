from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000049"
    council_name = "Glasgow City"
    elections = ["parl.2019-12-12"]

    def district_record_to_dict(self, record):
        # District that falls on Glasgow/N.Lanarkshire boundary change.
        # Ignore it for now.

        if record[0] == "NL43 (part)":
            return None

        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):

        # District that falls on Glasgow/N.Lanarkshire boundary change.
        # Ignore it for now.
        if record[0] == "NL43":
            return None

        # Doesn't appear in Districts shapefile
        if record[0] == "ES0117":
            return None

        # Corrections based on checking notice of polling place
        addresses = {
            "KE0310": "GARNETBANK PRIMARY SCHOOL, 231 RENFREW STREET",
            "SH1609": "SACRED HEART PRIMARY SCHOOL, 31 REID STREET",
            "SS0706": "ST ALBERT'S PRIMARY SCHOOL, 34 MAXWELL DRIVE",
            "SS1508": "ST BRIDE'S PRIMARY SCHOOL, 85 CRAIGIE STREET",
            "SS1607": "ST BRIGID'S PRIMARY SCHOOL, 4 GLENMORE AVENUE",
            "SS1908": "BLACKFRIARS PRIMARY SCHOOL, 310 CUMBERLAND STREET",
            "PR0318": "BUDHILL FAMILY LEARNING CENTRE PRE 5 CE CENTRE, 1A HALLHILL ROAD",
            "PR2621": "BLAIRTUMMOCK HOUSING ASSOCIATION, COMMUNITY HALL, 45 BOYNDIE ROAD",
            "SH0620": "CALEDONIA PRIMARY SCHOOL, 10 CALDERWOOD DRIVE",
            "SH0720": "CALEDONIA PRIMARY SCHOOL, 10 CALDERWOOD DRIVE",
            "SH3119": "EASTBANK ACADEMY, 26 ACADEMY STREET",
            "SH3319": "ST JOSEPH'S CHURCH HALL, 16 FULLARTON AVENUE",
            "KE1311": "BELHAVEN NURSERY, 54 KELVINSIDE AVENUE",
            "MS0516": "SCARAWAY NURSERY, 24 SHAPINSAY STREET",
            "MS3817": "SPRINGBURN LIBRARY, 10 KAY STREET",
            "PR3121": "RUCHAZIE COMMUNITY CENTRE, 441 GARTLOCH ROAD",
            "AN0114": "ANTONINE PRIMARY SCHOOL, 3 ABBOTSHALL AVENUE",
            "AN0814": "ST MARGARET'S PARISH CHURCH HALL, 2000 GREAT WESTERN ROAD",
            "AN2613": "SCOTSTOUN PRIMARY SCHOOL, 26 ORMISTON AVENUE, G14 9HN",
            "AN3312": "BROOMHILL COMMUNITY CHURCH OF THE NAZARENE, 95 BROOMHILL DRIVE (ENTER FROM NORBY ROAD)",
            "KE2523": "HYNDLAND PRIMARY SCHOOL, 36 FORTROSE STREET",
            "PK0506": "CRAIGTON PRIMARY SCHOOL, 5 MORVEN STREET",
            "PK0803": "LINTHAUGH NURSERY SCHOOL, 533 CROOKSTON ROAD",
            "PK0903": "LINTHAUGH NURSERY SCHOOL, 533 CROOKSTON ROAD",
            "PK1403": "LINTHAUGH NURSERY SCHOOL, 533 CROOKSTON ROAD",
            "PK2504": "LOURDES PRIMARY SCHOOL, 144 BERRYKNOWES ROAD",
            "PK2604": "LOURDES PRIMARY SCHOOL, 144 BERRYKNOWES ROAD",
            "PK3304": "NETHERCRAIGS (GLASGOW CLUB), 355 CORKERHILL ROAD",
            "SS0205": "IBROX PRIMARY SCHOOL, 40 HINSHELWOOD DRIVE",
        }

        rec = super().station_record_to_dict(record)

        if rec:
            try:
                rec["address"] = addresses[rec["internal_council_id"]]
                rec["location"] = None
                return rec
            except KeyError:
                return rec
