from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "E06000038"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019Reading.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019Reading.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "310078632":
            rec["postcode"] = "RG2 0NS"

        if uprn in [
            "310080475",  # RG304RX -> RG304RY : 75 St. Michael`s Road, Tilehurst, Reading
            "310077642",  # RG27EX -> RG27EZ : Flat 2, The Farmhouse, Sherfield Drive, Sherfield Drive, Reading
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "310015114",  # RG315AN -> RG48LP : Flat 9, 52 School Road, Tilehurst, Reading
            "310008459",  # RG303ES -> RG303QN : Flat 17 Priory Point, 36 Southcote Lane, Southcote, Reading
            "310055368",  # RG27RU -> RG303HY : White Barn, 45A Cressingham Road, Reading
            "310023684",  # RG17YJ -> RG17YG : 1 Prospect Cottages, Prospect Mews, Reading
            "310023686",  # RG17YJ -> RG17YG : 2 Prospect Cottages, Prospect Mews, Reading
            "310023687",  # RG17YJ -> RG17YG : 3 Prospect Cottages, Prospect Mews, Reading
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 == "RG30 3DZ":
            return None
        if (
            record.addressline1 == "Flat 1"
            and record.addressline2 == "6 Gosbrook Road"
            and record.addressline3 == "Caversham"
            and record.addressline4 == "Reading"
        ):
            return None

        return rec
