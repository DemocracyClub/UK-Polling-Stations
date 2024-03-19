from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWK"
    addresses_name = (
        "2024-05-02/2024-03-19T09:41:01.760435/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T09:41:01.760435/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003451291",  # ST. FAITHS VICARAGE, 62 RED POST HILL, LONDON
            "10096036520",  # FLAT 1, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036521",  # FLAT 2, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036522",  # FLAT 3, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036523",  # FLAT 4, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036524",  # FLAT 5, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036525",  # FLAT 6, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036526",  # FLAT 7, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036527",  # FLAT 8, SEACOLE COURT 62A, RED POST HILL, LONDON
            "10096036528",  # FLAT 9, SEACOLE COURT 62A, RED POST HILL, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SE16 6AZ",
            "SE5 0SY",
            "SE15 6BJ",
            "SE5 7HY",
        ]:
            return None
        return super().address_record_to_dict(record)
