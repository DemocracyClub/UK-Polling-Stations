from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000136"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019boston.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019boston.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100030738257":
            rec["postcode"] = "PE20 2NZ"
            rec["accept_suggestion"] = False

        if uprn in [
            "100032168500",  # PE229JN -> PE229JP : The Cottage, Hurn`s End, Old Leake, Boston
            "10008181290",  # PE202PT -> PE202PJ : C`van Sparrow Hall, Asperton Road, Wigtoft, Boston
            "10008186479",  # PE202PT -> PE202PS : Taumberland, Asperton Road, Swineshead, Boston, Lincs
            "10008186513",  # PE220QA -> PE220PX : Field Views, Freiston Ings Farm Lane, Freiston Ings, Boston, Lincs
            "10008187814",  # PE218QN -> PE218QR : 63 West Street, Boston, Lincs
            "200004465433",  # PE217LH -> PE217JU : White House Farm, Wyberton West Road, Wyberton, Boston, Lincs
            "200004467072",  # PE201EG -> PE218SH : 10 High Street, Kirton, Boston, Lincs
            "200004471567",  # PE220PG -> PE219RZ : Orchard Lea, Wainfleet Road, Freiston, Boston
            "200004473861",  # PE203QX -> PE203SZ : Fairways, Top Farm, Kirton Drove, Brothertoft, Boston, Lincs
            "200004475159",  # LN44QJ -> LN44QN : The Wheelwright Bungalow, Kirton Drove, Kirton Fen, Lincoln, Lincs
            "200004475193",  # PE201SN -> PE201SP : Smith`s Lodge, Holmes Road, Kirton Holme, Boston, Lincs
            "200004476439",  # PE219QR -> PE219QP : 160 Spilsby Road, Fishtoft, Boston, Lincs
        ]:
            rec["accept_suggestion"] = True

        return rec
