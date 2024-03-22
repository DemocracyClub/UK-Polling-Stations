from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2024-05-02/2024-03-22T10:01:04.870722/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-22T10:01:04.870722/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Plains Farm Youth and Community Centre, Grounds of Plains Farm Academy, Tudor Grove, Sunderland
        if record.polling_place_id == "18488":
            record = record._replace(
                polling_place_easting="438000",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "DH4 5HY",
            "SR2 0AQ",
            "SR2 7HZ",
            "SR2 0LE",
            "DH4 7RD",
            "SR4 8JF",
            "SR4 6NP",
            "SR6 9DY",
            "SR4 7SD",
            "SR4 0BT",
            "SR3 1XF",
            "SR2 9JG",
            "SR5 3EP",
            "DH4 4JH",
            "SR6 0NB",
            "SR2 8RA",
            "SR4 8HA",
            "SR4 8JU",
            "SR3 3QH",
        ]:
            return None

        return super().address_record_to_dict(record)
