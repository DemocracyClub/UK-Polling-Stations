from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2022-05-05/2022-03-01T15:11:53.624789/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-01T15:11:53.624789/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn.strip().lstrip("0") == "310088234":
            record = record._replace(addressline6="RG1 1SN")

        if record.addressline6 in [
            "RG30 4RX",
            "RG4 8ES",
            "RG2 7PS",
        ]:
            return None

        return super().address_record_to_dict(record)
