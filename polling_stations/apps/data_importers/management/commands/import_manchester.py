from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = "2021-03-29T13:39:43.070287/manchester_deduped.tsv"
    stations_name = "2021-03-29T13:39:43.070287/manchester_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        # Moston Methodist Church corner of Ilkley Street and Moston Lane Moston Manchester
        if record.polling_place_id == "9002":
            record = record._replace(
                polling_place_easting="387244", polling_place_northing="401944"
            )

        # Holy Trinity Church Hall Goodman Street Blackley Manchester M9 4BW
        if record.polling_place_id == "8840":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "77123789",  # 2 ALMOND STREET, MANCHESTER
            "77123796",  # 2 DAVY STREET, MANCHESTER
        ]:
            return None

        if record.addressline6 in [
            "M8 9AE",
            "M1 2PE",
            "M12 5PR",
            "M20 1LU",
            "M22 8BE",
            "M15 4TN",
            "M15 4TP",
            "M15 4TW",
            "M15 4TT",
            "M15 4TU",
        ]:
            return None

        return super().address_record_to_dict(record)
