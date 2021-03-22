from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUS"
    addresses_name = "2021-03-18T15:04:35.902256/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-18T15:04:35.902256/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Bingham Methodist Centre, Union Street, Bingham, Nottingham
        if record.polling_place_id == "5064":
            record = record._replace(polling_place_easting="470360")

        # Edwalton Church Hall, Vicarage Green, Edwalton
        if record.polling_place_id == "5244":
            record = record._replace(polling_place_easting="459770")

        # West Bridgford Baptist Church, Melton Road, West Bridgford
        if record.polling_place_id == "5252":
            record = record._replace(polling_place_easting="458380")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3040046829",  # WILLOW BANK, ZOUCH FARM, MAIN STREET, ZOUCH, LOUGHBOROUGH
            "3040055436",  # 1A THE COTTAGE, GOTHAM ROAD, EAST LEAKE, LOUGHBOROUGH
            "3040057547",  # WEST END, LANGAR ROAD, BARNSTONE, NOTTINGHAM
            "3040046757",  # WINDY RIDGE, LANGAR ROAD, BARNSTONE, NOTTINGHAM
            "3040052762",  # DUKERIES TEXTILES, 15A MELBOURNE ROAD, WEST BRIDGFORD, NOTTINGHAM
            "3040012196",  # 11 WILLOW ROAD, COTGRAVE, NOTTINGHAM
            "3040072549",  # PROPERTY ON FIRST AND SECOND FLOOR 43 MUSTERS ROAD, WEST BRIDGFORD
        ]:
            return None

        if record.addressline6 in ["NG11 6NY", "NG2 5JT"]:
            return None

        return super().address_record_to_dict(record)
