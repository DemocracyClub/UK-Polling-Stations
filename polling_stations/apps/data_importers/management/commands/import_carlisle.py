from data_importers.ems_importers import BaseXpressDCCsvInconsistentPostcodesImporter


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "CAR"
    addresses_name = (
        "2022-05-05/2022-04-13T10:19:44.591286/Democracy_Club__05May2022-2.CSV"
    )
    stations_name = (
        "2022-05-05/2022-04-13T10:19:44.591286/Democracy_Club__05May2022-2.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CA6 4FB",
            "CA2 7LS",
            "CA5 6JS",
            "CA3 9HN",
            "CA6 4LF",
            "CA2 4RE",
        ]:
            return None

        return super().address_record_to_dict(record)
