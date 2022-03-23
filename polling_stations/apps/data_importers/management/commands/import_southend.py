from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "SOS"

    addresses_name = (
        "2022-05-05/2022-03-23T11:58:06.809992/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-23T11:58:06.809992/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SS3 9QH",
            "SS9 5EW",
            "SS9 4RP",
            "SS2 6UY",
            "SS9 1LN",
            "SS9 1NH",
            "SS9 1RP",
            "SS9 1QY",
            "SS9 3BG",
        ]:
            return None

        return super().address_record_to_dict(record)
