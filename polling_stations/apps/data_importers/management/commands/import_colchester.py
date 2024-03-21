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
            record = record._replace(polling_place_postcode="CO2 8BA")

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
        ]:
            return None

        return super().address_record_to_dict(record)
