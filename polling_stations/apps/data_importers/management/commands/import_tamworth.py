from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = "2022-05-05/2022-03-02T14:26:27.337999/Tamworth_BC_Democracy_Club__05May2022.tsv"
    stations_name = "2022-05-05/2022-03-02T14:26:27.337999/Tamworth_BC_Democracy_Club__05May2022.tsv"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "394040617",  # 77C AMINGTON ROAD, TAMWORTH, B77 3LN
        ]:
            return None
        if record.addressline6 in ["B79 0BY"]:
            return None

        return super().address_record_to_dict(record)
