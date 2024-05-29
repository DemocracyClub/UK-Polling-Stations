from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = (
        "2024-07-04/2024-05-29T12:03:29.474027/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T12:03:29.474027/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070037178",  # LARK RISE, REDHILL, RUSHDEN, BUNTINGFORD
            "10023318781",  # OLD WESTMILL FARMHOUSE, WESTMILL LANE, ICKLEFORD, HITCHIN
            "10070041819",  # 2 RYE END COTTAGES, CODICOTE, HITCHIN
            "10070041818",  # 1 RYE END COTTAGES, CODICOTE, HITCHIN
            "10023322537",  # DUCKS NEST COTTAGE, NEWSELLS PARK STUD, BARKWAY, ROYSTON
            "10023322541",  # GRANGE COTTAGE, NEWSELLS PARK STUD, BARKWAY, ROYSTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SG8 8AD",
            # looks wrong
            "LU2 8NH",
            "SG5 1ET",
        ]:
            return None

        return super().address_record_to_dict(record)
