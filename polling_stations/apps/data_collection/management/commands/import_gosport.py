from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000088"
    addresses_name = (
        "parl.2019-12-12/Version 1/2019 PGE - Democracy_Club__12December2019gosport.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/2019 PGE - Democracy_Club__12December2019gosport.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "37013642",  # PO122BY -> PO123BY : Duncan Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Hood Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Onslow Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Ussher Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Beaufort Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Ramsey Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Rodney Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Cunningham Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Inman Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Nelson Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Oates Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Vian Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Yarmouth Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Keyes Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : JRAC Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Esmonde Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Whitworth Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Benbow Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Sommerville Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Phoebe Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Quiberon Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Salisbury Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Jervis Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Mountbatten Block, HMS Sultan, Military Road, Gosport, Hampshire
            "37042796",  # PO122BY -> PO123BG : The Wardroom, HMS Sultan, Military Road, Gosport, Hampshire
            "37013642",  # PO122BY -> PO123BY : Lefanu Block, HMS Sultan, Military Road, Gosport, Hampshire
        ]:
            rec["accept_suggestion"] = True

        return rec
