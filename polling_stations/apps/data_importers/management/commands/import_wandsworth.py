from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = (
        "2024-05-02/2024-03-14T08:27:43.083804/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-14T08:27:43.083804/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095441123",  # BASEMENT FLAT, 221 PUTNEY BRIDGE ROAD, LONDON
            "100022701958",  # 5 THURLEIGH MANSIONS 33 THURLEIGH ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SW12 9RF",
            "SW17 7BB",
        ]:
            return None

        return super().address_record_to_dict(record)
