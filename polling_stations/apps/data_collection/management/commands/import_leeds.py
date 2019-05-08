from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E08000035"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club_Leeds_Euro.26.4.2019.CSV"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club_Leeds_Euro.26.4.2019.CSV"
    )
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # user error report
        if record.pollingplaceid == "5804":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.580224, 53.852590, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "72665104",  # LS208NP -> LS209NP : SPRINGFIELD FARM Cross Lane
            "72660957",  # LS98BP -> LS99BP : 240 York Road
            "72040822",  # LS74EE -> LS73DU : FLAT 3 130 1ST FLR LEFT Chapeltown Road
            "72040823",  # LS74EE -> LS73DU : FLAT 4 130 1ST FLR RIGHT Chapeltown Road
            "72040824",  # LS74EE -> LS73DU : FLAT 5 130 2ND FLR Chapeltown Road
            "72744048",  # LS85AQ -> LS85AJ : 99 FLAT Roundhay Road
            "72686239",  # LS208FG -> LS208JJ : 7 ANNEXE Ridge Close
            "72660575",  # LS146HB -> LS146TY : School House Parklands High Schl, South Parkway
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "72746303",  # LS96AR -> LS96AG : Flat 3 29 Bellbrooke Place
            "72539799",  # LS133PW -> LS133PP : 8B Granhamthorpe
            "72008284",  # LS85BP -> LS97AB : 12 Ashton Place
            "72020737",  # LS83RN -> LS96AB : 1 Berkeley Mount
            "72201866",  # LS96AB -> LS83RP : 41 Strathmore Drive
            "72018898",  # LS96AG -> LS96AR : 40 Seaforth Avenue
            "72683687",  # LS96AG -> LS96AR : Flat 3 49 Seaforth Avenue
            "72719128",  # LS97AQ -> LS97AB : 2 Ashley Terrace
            "72084257",  # LS62DX -> LS62DU : 2 8 FALMER COTTAGE Grosvenor Mount
            "72084257",  # LS62DX -> LS62DU : 8 Grosvenor Mount
            "72203232",  # LS116EA -> LS116EW : 49 Rowland Road
            "72719179",  # LS116JE -> LS116HX : 1 Stratford Terrace
            "72663909",  # LS31BX -> LS31ER : 17 BASEMENT FLAT Victoria Terrace
            "72700117",  # LS61PY -> LS61QR : 27 Hyde Park Road
            "72383453",  # LS268SX -> LS268RE : 7 Quarry Hill
            "72043456",  # LS64DX -> LS64ED : 20A Monk Bridge Road
            "72337075",  # LS226SF -> LS226SH : 5 Spofforth Hill
            "72541837",  # LS278JT -> LS278JX : Crank Cottage Station Road
            "72334891",  # LS227TE -> LS227QH : Allanfield House Deighton Road
            "72222395",  # LS61DL -> LS61DR : FLAT 4 82 Victoria Road
            "72322167",  # LS254AQ -> LS254AF : New School House Great North Road
            "72720953",  # LS257JE -> LS257JD : 87 Flat Oxford Drive
            "72720954",  # LS257JE -> LS257JD : 87 The Stables Oxford Drive
            "72506861",  # WF102ET -> WF102HE : Flat 1 96 Leeds Road
            "72241127",  # LS146AX -> LS146DX : 855 Flat York Road
            "72748363",  # LS31BT -> LS31BU : 3 FLAT The Villa, Victoria Street
            "72545794",  # LS289JU -> LS289LD : Mistal House Adcock Bank Farm, Troydale Lane
            "72663318",  # LS260ET -> LS260FF : Cottage Springhead Park House, Park Lane
        ]:
            rec["accept_suggestion"] = False

        return rec
