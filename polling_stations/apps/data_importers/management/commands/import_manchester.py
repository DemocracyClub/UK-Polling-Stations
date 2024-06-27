from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2024-07-04/2024-05-31T13:02:19.239017/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T13:02:19.239017/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "77123789",  # 2 ALMOND STREET, MANCHESTER
            "77123796",  # 2 DAVY STREET, MANCHESTER
            "10095846092",  # 276B YEW TREE ROAD, MANCHESTER
            "10095846090",  # 276A YEW TREE ROAD, MANCHESTER
            "10070863520",  # CHORLTON PLACE CARE HOME, 290 WILBRAHAM ROAD, MANCHESTER
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

        # amendment from council:
        # old polling station: Manchester Oratory (St Chads Church), Cheetham Hill.
        # new polling station: Central Library, St Peters Square, Manchester, M2 5PD
        if record.polling_place_district_reference == "1DGA":
            record = record._replace(
                polling_place_id="14354",
                polling_place_name="Central Library",
                polling_place_address_1="St Peters Square",
                polling_place_address_2="",
                polling_place_address_3="Manchester",
                polling_place_address_4="",
                polling_place_postcode="M2 5PD",
                polling_place_easting="383864",
                polling_place_northing="397941",
                polling_place_uprn="",
                default_polling_place_id="2834",
            )
        return super().address_record_to_dict(record)
