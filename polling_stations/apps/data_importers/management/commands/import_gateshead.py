from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = "2021-04-26T17:25:33.216720/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-26T17:25:33.216720/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022984423",  # HIGH EIGHTON FARM HOUSE BLACK LANE, HARLOW GREEN, GATESHEAD
            "10024188004",  # 168 SHERIFFS HIGHWAY, GATESHEAD
            "100000029999",  # 125 ELLISON ROAD, GATESHEAD
            "10093488596",  # BULLERWELL HOUSE ASHTREE LANE, HIGH SPEN, ROWLANDS GILL
            "10070837301",  # 1A SPLIT CROW ROAD, GATESHEAD
            "10070836935",  # RESIDENTIAL ACCOMMODATION COACH AND HORSES INN DURHAM ROAD, BIRTLEY
        ]:
            return None

        if record.addressline6 in ["NE9 5XP", "NE9 6JR", "NE10 9RZ"]:
            return None

        return super().address_record_to_dict(record)
