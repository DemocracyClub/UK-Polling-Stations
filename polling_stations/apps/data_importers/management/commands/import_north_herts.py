from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = (
        "2024-05-02/2024-02-27T10:50:57.357829/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T10:50:57.357829/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Market Hill Rooms, Fish Hill, Royston, SG8 9JL
        # Council requested to use below postcode
        if record.polling_place_id == "9796":
            record = record._replace(polling_place_postcode="SG8 9LB")

        return super().station_record_to_dict(record)
