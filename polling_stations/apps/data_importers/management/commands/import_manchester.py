from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2024-05-02/2024-03-07T09:49:32.952597/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T09:49:32.952597/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Moston Methodist Church corner of Ilkley Street and Moston Lane
        if record.polling_place_id == "13774":
            record = record._replace(polling_place_easting="387238")
            record = record._replace(polling_place_northing="401949")

        # NEW POLLING STATION, East Didsbury Methodist Church, 496 Parrs Wood Road, East Didsbury, Manchester M20 5QQ
        if record.polling_place_id == "14080":
            record = record._replace(polling_place_easting="384958")
            record = record._replace(polling_place_northing="389941")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "77123789",  # 2 ALMOND STREET, MANCHESTER
            "77123796",  # 2 DAVY STREET, MANCHESTER
        ]:
            return None

        if record.addressline6 in [
            # split
            "M12 5PR",
            "M1 2PE",
            "M22 8BE",
            "M8 9AE",
            # suspect
            "M22 5BL",
            "M20 2NQ",
            "M4 7AA",
            "M8 4RB",
        ]:
            return None

        return super().address_record_to_dict(record)
