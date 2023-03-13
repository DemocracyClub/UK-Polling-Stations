from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHA"
    addresses_name = "2023-05-04/2023-03-13T11:03:51.149137/EC & Democracy Club Polling Place Lookup.tsv"
    stations_name = "2023-05-04/2023-03-13T11:03:51.149137/EC & Democracy Club Polling Place Lookup.tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10070073939",  # MANAGERS ACCOMMODATION 109 LEICESTER ROAD, MOUNTSORREL
            "10091071561",  # THE OLD FARM HOUSE, SCHOOL LANE, BIRSTALL, LEICESTER
        ]:
            return None
        if record.addressline6 in ["LE7 7GA"]:  # looks wrong
            return None
        return super().address_record_to_dict(record)
