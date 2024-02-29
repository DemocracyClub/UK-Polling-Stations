from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MON"
    addresses_name = (
        "2024-05-02/2024-02-29T19:06:00.935974/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-29T19:06:00.935974/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # postcode correction for:  Leisure Centre, Crossway Green, Chepstow, Monmouthshire, NP6 5LX
        # source: https://vinsights.co.uk/Business/225657
        if record.polling_place_id == "11172":
            record = record._replace(polling_place_postcode="NP16 5LX")

        # postcode correction for: Village Hall, Whitebrook, Monmouth, NP27 4TT
        # source: https://www.uk-hallhire.co.uk/halls/NP/74220.php
        if record.polling_place_id == "11458":
            record = record._replace(polling_place_postcode="NP25 4TT")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.polling_place_uprn.strip().lstrip("0")

        if uprn in [
            "10033357396",  # COED POETH COTTAGE, TREGARE, MONMOUTH
        ]:
            return None

        if record.addressline6.strip() in [
            # splits
            "NP7 5PW",
            "NP7 5LL",
            "NP26 4PQ",
            "NP7 7DH",
            "NP26 5SD",
            "NP7 7EE",
            "NP25 5DJ",
            "NP7 8RP",
            "NP25 5BG",
            "NP26 4HL",
            "NP26 4NB",
            "NP25 3LP",
            "NP25 4TS",
            "NP7 5LF",
            "NP7 9HS",
            "NP25 4AE",
            "NP7 9EU",
            "NP16 5BE",
            "NP26 3AR",
            "NP7 7DW",
            "NP16 6HX",
            "NP7 9EG",
            "NP25 3BQ",
            "NP16 6NF",
            "NP7 7EY",
            # looks wrong
            "NP26 4RL",
        ]:
            return None

        return super().address_record_to_dict(record)
