from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = "2021-10-07/SouthKestevenDemocracy_Club__28October2021.tsv"
    stations_name = "2021-10-07/SouthKestevenDemocracy_Club__28October2021.tsv"
    elections = ["2021-10-28"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030946733",  # TOLL BAR HOUSE UFFINGTON ROAD, STAMFORD
            "100030901277",  # 64 BURGHLEY STREET, BOURNE
            "100030901276",  # 60 BURGHLEY STREET, BOURNE
            "10007275381",  # FLAT 59 LONDON ROAD, GRANTHAM
            "10007276237",  # 86 THE DEEPINGS CARAVAN PARK TOWNGATE EAST, MARKET DEEPING
        ]:
            return None

        if record.addressline6 in [
            "NG32 1AT",
            "NG33 4JQ",
            "NG33 4HE",
            "NG33 4SP",
            "PE9 4PE",
            "PE10 0AA",
            "PE10 9RP",
            "PE9 2XG",
            "NG32 3AU",
            "NG32 3AY",
            "NG23 5HN",
            "NG32 2LW",
            "NG31 8RJ",
            "NG31 9JZ",
            "NG31 7QP",
            "NG31 8AB",
            "NG31 8NH",
        ]:
            return None

        return super().address_record_to_dict(record)
