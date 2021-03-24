from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOI"
    addresses_name = "2021-03-19T11:17:13.350243/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-19T11:17:13.350243/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002421652",  # FLAT ABOVE CLUBHOUSE SUTTON GREEN GOLF CLUB NEW LANE, SUTTON GREEN, WOKING
            "200000218826",  # THE BUNGALOW DAWNEY HILL, PIRBRIGHT
            "200000201900",  # ASAD, MAYBURY HILL, WOKING
        ]:
            return None

        if record.addressline6 in ["KT14 6LT", "GU22 8AF"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Horsell Evangelical Church High Street Horsell Woking GU21 3SZ
        if record.polling_place_id == "4159":
            record = record._replace(polling_place_postcode="GU21 4SZ")

        return super().station_record_to_dict(record)
