from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOI"
    addresses_name = (
        "2024-05-02/2024-02-25T13:24:35.080186/Democracy_Club__02May2024.tsv - WBC.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-25T13:24:35.080186/Democracy_Club__02May2024.tsv - WBC.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000218826",  # THE BUNGALOW DAWNEY HILL, PIRBRIGHT
            "10002428855",  # FLAT 7, THE OLD BREW HOUSE 130-132, HIGH STREET, OLD WOKING, WOKING
            "200000216418",  # THORLEY COTTAGE, PYRFORD ROAD, WOKING
            "100061656800",  # HEDGE COTTAGE, SAUNDERS LANE, WOKING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "KT14 6LT",
            "GU22 8AF",
            "GU21 2NJ",
            # looks wrong
            "KT15 3QA",
            "KT15 3QD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Horsell Evangelical Church High Street Horsell Woking GU21 3SZ
        if record.polling_place_id == "5299":
            record = record._replace(polling_place_postcode="GU21 4SZ")

        return super().station_record_to_dict(record)
