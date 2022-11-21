from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2022-12-15/2022-11-21T12:49:06.121803/Democracy_Club__15December2022.CSV"
    )
    stations_name = (
        "2022-12-15/2022-11-21T12:49:06.121803/Democracy_Club__15December2022.CSV"
    )
    elections = ["2022-12-15"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "M32 0SF",
            "M41 9AS",
            "M41 6JU",
        ]:
            return None

        return super().address_record_to_dict(record)
