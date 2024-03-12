from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRT"
    addresses_name = (
        "2024-05-02/2024-03-12T10:53:14.351979/Democracy_Club__02May2024.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-12T10:53:14.351979/Democracy_Club__02May2024.csv"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # St Mary Magdalenes Church Hall, 87 Dingleway, Appleton, Warrington WA4 3AG
        if record.polling_place_id == "2142":
            record = record._replace(
                polling_place_easting="362050",
                polling_place_northing="385487",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WA4 5PQ",
            # suspect
            "WA5 3BF",
        ]:
            return None
        return super().address_record_to_dict(record)
