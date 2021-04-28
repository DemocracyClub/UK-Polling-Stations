from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THA"
    addresses_name = "2021-04-28T10:23:11.064744/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-28T10:23:11.064744/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013308976",  # FLAT AT BELLE VUE TAVERN PEGWELL ROAD, RAMSGATE
        ]:
            return None

        if record.addressline6 in ["CT10 1QL", "CT10 3AE", "CT12 5BX", "CT9 4BT"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # All Saints Church Hall All Saints Avenue Margate Kent CT9 5LQ
        if record.polling_place_id == "6427":
            record = record._replace(polling_place_postcode="CT9 5QL")

        return super().station_record_to_dict(record)
