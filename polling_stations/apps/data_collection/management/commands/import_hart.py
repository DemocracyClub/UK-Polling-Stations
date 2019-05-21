from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000089"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Hart.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Hart.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008959585",  # GU179LW -> GU466AT : Leafy Oak Farmhouse, Cobbetts Lane, Blackwater, Camberley
            "200001000440",  # RG278BU -> RG291JR : Chevertons Farm, Odiham Road, Winchfield, Hook
            "10008948691",  # RG278EF -> RG278SH : Taplins Farm Stables, Church Lane, Hartley Wintney, Hook
            "200001006098",  # GU105HJ -> RG291TL : Quern Farm, Well Road, Crondall, Farnham
            "100060406353",  # GU527UA -> GU467RX : 94A Reading Road South, Fleet, Hampshire
            "200001000332",  # RG279JJ -> RG278JD : The Annexe, 1 Yew Tree Cottage, Hook Common, Hook
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "2487":
            record = record._replace(polling_place_easting="479224")
            record = record._replace(polling_place_northing="154016")

        return super().station_record_to_dict(record)
