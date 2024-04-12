from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLG"
    addresses_name = (
        "2024-05-02/2024-04-12T11:24:40.557900/Democracy_Club__02May2024 (24).tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T11:24:40.557900/Democracy_Club__02May2024 (24).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # splits
            "SL1 2LT",
            "SL1 1LU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Centre, Farnham Road, Slough, SL1 4UT
        # postcode in a wrong column, just moving it to the right place
        if record.polling_place_id == "2567":
            record = record._replace(polling_place_postcode="SL1 4UT")

        return super().station_record_to_dict(record)
