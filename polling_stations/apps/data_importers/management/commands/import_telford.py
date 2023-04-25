from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TFW"
    addresses_name = (
        "2023-05-04/2023-04-20T13:49:05.049834/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-20T13:49:05.049834/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "452098161",  # AQUALATE MANOR, STAFFORD ROAD, NEWPORT
            "200001754669",  # CHARTLEY, CHURCH ASTON, NEWPORT
            "452098134",  # CARAVAN 3 GREENFIELDS COUNTRY STORE STATION ROAD, DONNINGTON, TELFORD
            "452063031",  # HOMECROFT, ADMASTON, TELFORD
            "452084193",  # MEESE COTTAGE, HOWLE, NEWPORT
            "452063475",  # 10 RUSHMOOR LANE, BRATTON, TELFORD
            "452094687",  # THE RIDGEWAYS, THE HEM, SHIFNAL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TF10 7ZN",
            "TF8 7NN",
            "TF2 8SF",
            "TF10 7RG",
            "TF4 3JZ",
            "TF2 9HF",
            "TF3 4LY",  # BEEFEATER EUSTON WAY, TELFORD TOWN CENTRE, TELFORD
        ]:
            return None

        return super().address_record_to_dict(record)
