from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NED"
    addresses_name = (
        "2021-04-19T12:06:33.960290/EC & Democracy Club Polling Place Lookup.csv"
    )
    stations_name = (
        "2021-04-19T12:06:33.960290/EC & Democracy Club Polling Place Lookup.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034033018",  # THE SIDINGS, ASHOVER ROAD, WOOLLEY MOOR, ALFRETON
        ]:
            return None

        return super().address_record_to_dict(record)
