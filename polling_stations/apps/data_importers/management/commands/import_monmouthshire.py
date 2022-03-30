from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MON"
    addresses_name = (
        "2022-05-05/2022-03-30T13:32:24.067252/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-30T13:32:24.067252/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Leisure Centre, Crossway Green, Chepstow, Monmouthshire
        if record.polling_place_id == "9987":
            # source: https://vinsights.co.uk/Business/225657
            record = record._replace(polling_place_postcode="NP16 5LX")  # was NP6 5LX

        # Village Hall, Whitebrook, Monmouth
        if record.polling_place_id == "10097":
            # source: https://www.uk-hallhire.co.uk/halls/NP/74220.php
            record = record._replace(polling_place_postcode="NP25 4TT")  # was NP27 4TT

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in [
            "NP25 5DJ",
            "NP7 5PW",
            "NP7 7DH",
            "NP16 5BE",
            "NP25 3LP",
            "NP26 4NB",
            "NP26 4AG",
            "NP7 9EU",
            "NP26 4PQ",
            "NP7 5LF",
            "NP25 5BG",
            "NP7 7DW",
            "NP25 5UF",
            "NP7 5LL",
            "NP26 5SD",
            "NP26 3NU",
            "NP7 7EY",
            "NP16 6HX",
            "NP26 4HL",
            "NP7 8RP",
            "NP7 7EE",
            "NP25 3BQ",
            "NP26 3AR",
            "NP7 5LB",
            "NP25 4TS",
            "NP25 4AE",
            "NP7 9EG",
        ]:
            return None  # split

        if record.addressline6.strip() in [
            "NP26 4RL",  # four properties a long way from their stations
        ]:
            return None

        return super().address_record_to_dict(record)
