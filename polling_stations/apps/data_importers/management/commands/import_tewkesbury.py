from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = "2023-05-04/2023-04-14T11:29:27.195526/Democracy_Club__04May2023_Tewkesbury Borough.tsv"
    stations_name = "2023-05-04/2023-04-14T11:29:27.195526/Democracy_Club__04May2023_Tewkesbury Borough.tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100121260162",  # BAMFURLONG FARM, BAMFURLONG LANE, CHELTENHAM
        ]:
            return None

        return super().address_record_to_dict(record)
