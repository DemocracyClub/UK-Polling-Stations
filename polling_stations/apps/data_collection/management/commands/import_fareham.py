from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000087"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "5854":
            # Titchfield Parish Rooms
            record = record._replace(polling_place_postcode="PO14 4AQ")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        # correction from the EC
        if record.polling_place_district_reference.strip() == "ST1":
            record = record._replace(polling_place_id="5876")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.lstrip("0")

        if uprn == "100060367957":
            return None  # conflation of "123 Locks Road, Lock Heath" and "123 Locks Heath Parks Road"

        if uprn in [
            "100060360780",  # PO144LJ -> PO144LL : 387 Warsash Road, Titchfield Common, Fareham
            "100060356905",  # PO144QS -> PO144QJ : 25 Steeple Way, Titchfield, Fareham
            "100060370702",  # SO317AX -> SO317HB : 175 Swanwick Lane, Lower Swanwick, Southampton
            "100060363942",  # SO317EL -> SO317EN : 133 Bridge Road, Sarisbury, Southampton
            "100060360220",  # PO142LA -> PO142JU : 15 Vicarage Lane, Stubbington, Fareham
        ]:
            rec["accept_suggestion"] = True

        return rec
