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

        # The following two coordinate changes are from the council:

        # NEW POLLING STATION, Temporary Building, Sun in September Car Park, 588 Burnage Lane, Burnage M19 1NA
        if record.polling_place_id == "13482":
            record = record._replace(polling_place_easting="386076")
            record = record._replace(polling_place_northing="391679")
        # NEW POLLING STATION, Temporary Building, Corner of Royal Oak Road / Spark Street, Manchester M23 1FB
        if record.polling_place_id == "13413":
            record = record._replace(polling_place_easting="381014")
            record = record._replace(polling_place_northing="389164")

        # The following is station change from the council:
        # old: Sandilands Primary School, Infant Department, Wendover Road, Brooklands, Manchester M23 9JX
        # new (existing): Church of the Nazarene, Wendover Road, Brooklands, Manchester M23 9FN
        if record.polling_place_id == "13457":
            record = record._replace(
                polling_place_id="13470",
                polling_place_name="Church of the Nazarene",
                polling_place_address_1="Wendover Road",
                polling_place_address_2="",
                polling_place_address_3="Brooklands",
                polling_place_address_4="Manchester",
                polling_place_postcode="M23 9FN",
                polling_place_easting="379820",
                polling_place_northing="389788",
                polling_place_uprn="",
                default_polling_place_id="614",
            )

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
