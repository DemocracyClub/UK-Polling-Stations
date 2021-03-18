from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAS"
    addresses_name = "2021-03-17T16:31:21.505378/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-17T16:31:21.505378/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062577569",  # THE ROYAL ALBERT, 293 BATTLE ROAD, ST. LEONARDS-ON-SEA
            "10002500023",  # BEECH VIEW, CAMPKIN GARDENS, ST. LEONARDS-ON-SEA
            "10070607789",  # 120 BATTLE ROAD, ST. LEONARDS-ON-SEA
            "100062577571",  # NUMBER 46 GUEST HOUSE, 46 CAMBRIDGE GARDENS, HASTINGS
            "10002501567",  # 285 ELPHINSTONE ROAD, HASTINGS
        ]:
            return None

        if record.addressline6 in ["TN38 9EL", "TN37 7JL"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Downs Farm Community Centre Crowborough Road Hastings TN35 5EA
        if record.polling_place_id == "887":
            record = record._replace(polling_place_postcode="TN35 5EE")

        return super().station_record_to_dict(record)
