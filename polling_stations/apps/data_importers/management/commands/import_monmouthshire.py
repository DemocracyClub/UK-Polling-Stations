from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "MON"
    addresses_name = (
        "2024-05-02/2024-03-18T11:47:38.967548/Democracy_Club__02May2024 - Updated.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T11:47:38.967548/Democracy_Club__02May2024 - Updated.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
        "polling_place_address_2",
    ]

    def station_record_to_dict(self, record):
        # postcode correction for: Leisure Centre, Crossway Green, Chepstow, Monmouthshire, NP6 5LX
        if record.polling_place_id == "11172":
            record = record._replace(polling_place_postcode="NP16 5LX")

        # postcode correction for: Village Hall, Whitebrook, Monmouth, NP27 4TT
        if record.polling_place_id == "11458":
            record = record._replace(polling_place_postcode="NP25 4TT")

        # postcode correction for: Rectory Hall, Llanfair Kilgeddin, NP4 9BB
        if record.polling_place_id == "11333":
            record = record._replace(polling_place_postcode="NP7 9BD")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.polling_place_uprn.strip().lstrip("0")

        if uprn in [
            "10033357396",  # COED POETH COTTAGE, TREGARE, MONMOUTH
        ]:
            return None

        if record.addressline6.strip() in [
            # splits
            "NP7 5LL",
            "NP25 5BG",
            "NP7 7DH",
            "NP26 4PQ",
            "NP25 5DJ",
            "NP7 8RP",
            "NP16 5BE",
            "NP7 5PW",
            "NP7 9EU",
            "NP26 5SD",
            "NP25 3LP",
            "NP7 5LF",
            "NP26 4NB",
            "NP7 9HS",
            "NP7 7EE",
            "NP26 3AR",
            "NP25 3BQ",
            "NP26 4HL",
            "NP16 6NF",
            "NP7 7EY",
            "NP16 6HX",
            "NP7 9EG",
            "NP7 7DW",
            "NP25 4AE",
            "NP25 4TS",
        ]:
            return None

        return super().address_record_to_dict(record)
