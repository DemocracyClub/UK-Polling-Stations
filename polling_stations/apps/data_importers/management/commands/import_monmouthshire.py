from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MON"
    addresses_name = (
        "2024-07-04/2024-06-07T16:12:18.330990/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T16:12:18.330990/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # postcode correction for: Leisure Centre, Crossway Green, Chepstow, Monmouthshire, NP6 5LX
        if record.polling_place_id == "11598":
            record = record._replace(polling_place_postcode="NP16 5LX")

        # postcode correction for: Village Hall, Whitebrook, Monmouth, NP27 4TT
        if record.polling_place_id == "11883":
            record = record._replace(polling_place_postcode="NP25 4TT")

        # postcode correction for: Rectory Hall, Llanfair Kilgeddin, NP4 9BB
        if record.polling_place_id == "11758":
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
            "NP16 5BE",
            "NP7 5PW",
            "NP25 5BG",
            "NP26 4PQ",
            "NP7 7DH",
            "NP7 5LF",
            "NP7 5LL",
            "NP7 9EU",
            "NP25 5DJ",
            "NP7 7DW",
            "NP25 3BQ",
            "NP7 8RP",
            "NP25 4AE",
            "NP26 3AR",
            "NP25 4TS",
            "NP16 6NF",
            "NP26 4HL",
            "NP26 5SD",
            "NP16 6HX",
            "NP25 3LP",
            "NP7 7EY",
            "NP7 9HS",
            "NP7 7EE",
            "NP26 4NB",
            "NP7 9EG",
        ]:
            return None

        return super().address_record_to_dict(record)
