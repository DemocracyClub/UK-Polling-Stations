from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MON"
    addresses_name = (
        "2026-05-07/2026-02-25T13:17:13.002236/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-25T13:17:13.002236/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # postcode correction for: Leisure Centre, Crossway Green, Chepstow, Monmouthshire, NP6 5LX
        if record.polling_place_id == "13008":
            record = record._replace(polling_place_postcode="NP16 5LX")

        # postcode correction for: Village Hall, Whitebrook, Monmouth, NP27 4TT
        if record.polling_place_id == "13237":
            record = record._replace(polling_place_postcode="NP25 4TT")

        # postcode correction for: Rectory Hall, Llanfair Kilgeddin, NP4 9BB
        if record.polling_place_id == "13055":
            record = record._replace(polling_place_postcode="NP7 9BD")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.polling_place_uprn.strip().lstrip("0")

        if uprn in [
            "10033356635",  # FELLBANK, VEDDW, DEVAUDEN, CHEPSTOW
            "10033347903",  # KAIDEX, PERCUS BARN, DEVAUDEN, CHEPSTOW
        ]:
            return None

        if record.addressline6.strip() in [
            # splits
            "NP25 4AE",
            "NP7 5LF",
            "NP26 5SD",
            "NP16 6HX",
            "NP25 5DJ",
            "NP16 5BE",
            "NP7 8RP",
            "NP7 7EY",
            "NP7 5LL",
            "NP7 5PW",
            "NP26 4PQ",
            "NP7 7DH",
            "NP7 9EU",
            "NP26 4NB",
            "NP7 9HS",
            "NP7 7DW",
            "NP7 7EE",
            "NP7 9EG",
            "NP25 4TS",
            "NP25 3LP",
            "NP26 3AR",
            "NP16 6NF",
        ]:
            return None

        return super().address_record_to_dict(record)
