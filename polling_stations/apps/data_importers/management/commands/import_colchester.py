from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2024-05-02/2024-03-01T11:57:47.053594/Democracy_Club__02May2024 (7).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-01T11:57:47.053594/Democracy_Club__02May2024 (7).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Old Heath Community Centre, D'Arcy Road, Old Heath, Colchester, CO2 8BB
        if record.polling_place_id == "12587":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER
            "10095445911",  # 32D MAYPOLE GREEN ROAD, COLCHESTER
        ]:
            return None
        if record.addressline6 in [
            # split
            "CO2 8BU",
            "CO4 5LG",
            "CO6 1HA",
            # suspect (waiting on council response)
            "CO4 5HG",
            "CO4 6AU",
            "CO4 6AW",
            "CO4 6AX",
            "CO4 6BE",
            "CO4 6BG",
            "CO4 6BH",
            "CO4 6BP",
            "CO4 6BS",
            "CO4 6BD",
            "CO4 6BB",
            "CO4 6BF",
            "CO4 6BJ",
            "CO4 6BL",
            "CO4 6BN",
            "CO4 6BQ",
            "CO4 6BU",
            "CO4 6BX",
            "CO4 6AY",
            "CO4 6BR",
            "CO4 6BT",
            "CO4 6BW",
            "CO4 6BY",
            "CO4 6BZ",
            "CO4 6DB",
            "CO4 6DH",
        ]:
            return None

        return super().address_record_to_dict(record)
