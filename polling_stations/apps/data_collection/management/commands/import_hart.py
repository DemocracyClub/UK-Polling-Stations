from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000089"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Hart.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Hart.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10093265032", "100060398295", "10093264107"]:
            return None

        if uprn in [
            "10008959585",  # GU179LW -> GU466AT : Leafy Oak Farmhouse, Cobbetts Lane, Blackwater, Camberley
            "200001000440",  # RG278BU -> RG291JR : Chevertons Farm, Odiham Road, Winchfield, Hook
            "10008948691",  # RG278EF -> RG278SH : Taplins Farm Stables, Church Lane, Hartley Wintney, Hook
            "200001006098",  # GU105HJ -> RG291TL : Quern Farm, Well Road, Crondall, Farnham
            "100060406353",  # GU527UA -> GU467RX : 94A Reading Road South, Fleet, Hampshire
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        # Hart Leisure Centre
        if record.polling_place_id == "2903":
            record = record._replace(polling_place_easting="479224")
            record = record._replace(polling_place_northing="154016")

        return super().station_record_to_dict(record)
