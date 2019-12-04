from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000083"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019tewk.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019tewk.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code == "GL52 5QG":
            rec["postcode"] = "GL52 9QG"
            rec["accept_suggestion"] = False

        if uprn in ["10090024267"]:
            return None

        if uprn in [
            "10013762393",  # GL528SA -> GL528DQ : The Manor House, Cleeveway Manor, Evesham Road, Bishops Cleeve, Cheltenham, Glos
            "100121258121",  # GL29PQ -> GL29PU : The Cottage, Tewkesbury Road, Twigworth, Gloucester
            "200004335463",  # WR127ND -> WR127NE : Liberty Farm, Stanton, Broadway
            "200004330125",  # WR127NQ -> WR127ND : New House Farm, Stanton Road, Stanton, Broadway, Glos
            "10067629295",  # GL545PP -> GL545NY : 2 Millhampost Barn, Stanway, Cheltenham, Glos
            "10090023401",  # GL206JL -> GL208GN : 8 Styles Close, Northway, Tewkesbury, Glos
            "200004329486",  # GL510TL -> GL510TW : Brooklaines Farm, Barrow, Boddington, Cheltenham, Glos
            "200004331100",  # GL206JL -> GL206JD : The Granary, 1 Greenacres, Twyning, Tewkesbury, Glos
            "100121258576",  # GL205PR -> GL205PP : 2 Kings Head Cottages, Barton Street, Tewkesbury, Glos
            "100120553581",  # GL545QP -> GL545AB : Cotmore, Langley Road, Winchcombe, Cheltenham, Glos
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200004318039",  # GL28DQ -> GL528DH : Fairie Meade, 5 The Green, Highnam, Gloucester
            "10090020563",  # WR117TR -> WR117QN : 3 Raymeadow Cottages, Dumbleton, Evesham, Worcestershire
            "200004319980",  # GL29LS -> GL510TW : Church House, Church Lane, Norton, Gloucester
            "10067627280",  # GL205PP -> GL206DL : 2 Tysoes Court, 5A Barton Street, Tewkesbury, Glos
        ]:
            rec["accept_suggestion"] = False

        return rec
