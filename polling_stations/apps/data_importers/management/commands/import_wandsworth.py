from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = (
        "2024-07-04/2024-06-10T13:16:47.467544/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T13:16:47.467544/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095441123",  # BASEMENT FLAT, 221 PUTNEY BRIDGE ROAD, LONDON
            "100022701958",  # 5 THURLEIGH MANSIONS 33 THURLEIGH ROAD, LONDON
            "100023328601",  # THE COTTAGE, MAGDALEN ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SW12 9RF",
            "SW17 7BB",
        ]:
            return None

        return super().address_record_to_dict(record)
