from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWD"
    addresses_name = (
        "2022-05-05/2022-03-08T10:01:03.456828/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-08T10:01:03.456828/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090042967",  # 2 COMET WAY, WROUGHTON, SWINDON
            "10094328819",  # 170A RODBOURNE ROAD, SWINDON
            "100121344239",  # CONLON, UNIT 16 GALTON WAY, KENDRICK INDUSTRIAL ESTATE, SWINDON
            "200002920576",  # 549A CRICKLADE ROAD, SWINDON
        ]:
            return None

        if record.addressline6 in [
            "SN25 3LR",
            "SN25 3EN",
            "SN6 7JY",
            "SN3 5EP",
        ]:
            return None

        return super().address_record_to_dict(record)
