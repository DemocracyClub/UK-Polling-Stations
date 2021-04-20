from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2021-04-12T09:27:54.464494/Conwy New Democracy_Club__06May2021_10.04.2021.CSV"
    )
    stations_name = (
        "2021-04-12T09:27:54.464494/Conwy New Democracy_Club__06May2021_10.04.2021.CSV"
    )
    elections = ["2021-05-06"]
    csv_encoding = "latin1"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "LL26 0RW",
            "LL24 0LP",
            "LL26 0YU",
            "LL25 0HQ",
            "LL32 8PN",
            "LL32 8HW",
            "LL31 9EQ",
            "LL30 1NT",
            "LL31 9LG",
            "LL26 0YS",
            "LL30 1YQ",
            "LL30 1YY",
            "LL30 2DP",
            "LL28 4HG",
            "LL29 9YP",
            "LL22 7DT",
            "LL22 8UG",
            "LL21 9NY",
            "LL21 9PH",
        ]:
            return None  # split

        if record.addressline6 in [
            "LL22 8FB",  # embedded in another polling district
        ]:
            return None

        if record.property_urn.lstrip(" 0") in [
            "10023132438",  # embedded in another polling district
        ]:
            return None

        return super().address_record_to_dict(record)
