from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000035"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019leeds.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019leeds.CSV"
    elections = ["parl.2019-12-12"]

    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Portable building on land opposite 49 Aire Road
        if record.polling_place_id == "7234":
            rec["location"] = Point(-1.39239, 53.94110, srid=4326)

        # user error report #215
        # Guiseley AFC
        if record.polling_place_id == "7894":
            rec["location"] = None

        # user error report #219
        # All Souls Church
        if record.polling_place_id == "7329":
            rec["location"] = None

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "WF3 3LR",
            "LS14 6TY",
            "LS15 4NA",
        ]:
            return None

        if uprn in [
            "72040822",  # LS74EE -> LS73DU : FLAT 3 130 1ST FLR LEFT Chapeltown Road
            "72040823",  # LS74EE -> LS73DU : FLAT 4 130 1ST FLR RIGHT Chapeltown Road
            "72040824",  # LS74EE -> LS73DU : FLAT 5 130 2ND FLR Chapeltown Road
            "72660957",  # LS98BP -> LS99BP : 240 York Road
            "72744048",  # LS85AQ -> LS85AJ : 99 FLAT Roundhay Road
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "72008284",  # LS85BP -> LS97AB : 12 Ashton Place
            "72043456",  # LS64DX -> LS64ED : 20A Monk Bridge Road
            "72084257",  # LS62DX -> LS62DU : 2 8 FALMER COTTAGE Grosvenor Mount
            "72084257",  # LS62DX -> LS62DU : 8 Grosvenor Mount
            "72222395",  # LS61DL -> LS61DR : FLAT 4 82 Victoria Road
            "72241127",  # LS146AX -> LS146DX : 855 Flat York Road
            "72334891",  # LS227TE -> LS227QH : Allanfield House Deighton Road
            "72337075",  # LS226SF -> LS226SH : 5 Spofforth Hill
            "72506861",  # WF102ET -> WF102HE : Flat 1 96 Leeds Road
            "72539799",  # LS133PW -> LS133PP : 8B Granhamthorpe
            "72541837",  # LS278JT -> LS278JX : Crank Cottage Station Road
            "72545794",  # LS289JU -> LS289LD : Mistal House Adcock Bank Farm, Troydale Lane
            "72663909",  # LS31BX -> LS31ER : 17 BASEMENT FLAT Victoria Terrace
            "72700117",  # LS61PY -> LS61QR : 27 Hyde Park Road
            "72719128",  # LS97AQ -> LS97AB : 2 Ashley Terrace
            "72719179",  # LS116JE -> LS116HX : 1 Stratford Terrace
            "72720953",  # LS257JE -> LS257JD : 87 Flat Oxford Drive
        ]:
            rec["accept_suggestion"] = False

        return rec
