from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDB"
    addresses_name = (
        "2022-05-05/2022-03-22T12:48:17.017593/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-22T12:48:17.017593/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093036996",  # 40A STANLEY ROAD, ILFORD
            "10094819765",  # 5 PORTLAND TERRACE, ILFORD
            "10094820912",  # 6 PORTLAND TERRACE, ILFORD
            "10094821357",  # FLAT 1, 705B HIGH ROAD, ILFORD
            "10094821358",  # FLAT 2, 705B HIGH ROAD, ILFORD
            "10094821359",  # 705C HIGH ROAD, ILFORD
        ]:
            return None
        if record.addressline6 in [
            "IG5 0FF",  # embedded in another area
            "IG6 3FA",  # embedded in another area
            # split
            "IG1 2FP",
            "IG1 4SS",
            "IG5 0QA",
        ]:
            return None

        return super().address_record_to_dict(record)
