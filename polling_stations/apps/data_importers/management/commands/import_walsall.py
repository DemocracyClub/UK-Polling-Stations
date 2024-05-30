from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = (
        "2024-07-04/2024-05-30T10:48:52.727524/Democracy_Club__04July2024 (1).tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T10:48:52.727524/Democracy_Club__04July2024 (1).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071349802",  # 659A WALSALL ROAD, WEDNESBURY
            "100071109642",  # 124 GOUGH STREET, WILLENHALL
            "10090065467",  # 123A GOUGH STREET, WILLENHALL
            "10090065466",  # 123 GOUGH STREET, WILLENHALL
            "100071062219",  # 240 INGRAM ROAD, WALSALL
            "100071062221",  # 242 INGRAM ROAD, WALSALL
            "200003317397",  # CHRIST CHURCH RECTORY, BLAKENALL HEATH, WALSALL
            "10013664575",  # 52 MATTESLEY COURT, CRESSWELL CRESCENT, WALSALL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WV12 4BZ",
            "WS1 3LD",
            "WS3 2DX",
            # look wrong
            "WS2 0HS",
            "WS3 4NX",
            "WS3 4NT",
            "WS10 7TG",
            "WV13 2BG",
        ]:
            return None

        return super().address_record_to_dict(record)
