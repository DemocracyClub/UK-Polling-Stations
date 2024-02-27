from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUS"
    addresses_name = (
        "2024-05-02/2024-02-14T11:48:41.864356/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-02-14T11:48:41.864356/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Bingham Methodist Centre, Union Street, Bingham, Nottingham
        if record.polling_place_id == "6285":
            record = record._replace(polling_place_postcode="NG13 8AD")
            record = record._replace(polling_place_easting="470368")

        # Edwalton Church Hall, Vicarage Green, Edwalton
        if record.polling_place_id == "6145":
            record = record._replace(polling_place_postcode="NG12 4AP")
            record = record._replace(polling_place_easting="459770")

        # West Bridgford Baptist Church, Melton Road, West Bridgford
        if record.polling_place_id == "6290":
            record = record._replace(polling_place_easting="458385")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3040046674"  # WATERS EDGE, ZOUCH FARM, MAIN STREET, ZOUCH, LOUGHBOROUGH
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG13 8GP",
            "NG2 5JT",
            "NG13 8DT",
        ]:
            return None

        return super().address_record_to_dict(record)
