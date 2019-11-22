from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000090"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019havant.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019havant.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062455644",  # PO88BB -> PO78NU : Plough & Barleycorn, Tempest Avenue, Cowplain, Waterlooville, Hampshire
            "10013680951",  # PO107NH -> PO107DN : 1E St James Road, Emsworth, Hampshire
            "10013675502",  # PO89UB -> PO89GX : 7A The Kestrels, 76 Eagle Avenue, Waterlooville, Hampshire
            "10013679840",  # PO93EZ -> PO95EZ : 41 Tyler House, Bishopstoke Road, Havant, Hampshire
            "10013679413",  # PO92DT -> PO93DT : 2 Mead Terrace, Hooks Lane, Bedhampton, Havant, Hampshire
        ]:
            rec["accept_suggestion"] = True

        return rec
