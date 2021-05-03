from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = "2021-03-24T10:25:10.922382/Kirklees Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-24T10:25:10.922382/Kirklees Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # New Mill Working Mens Club Sheffield Road New Mill Holmfirth HD9 7JT
        if record.polling_place_id == "14458":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Roberttown Community Centre
        # Entrance is on Church Rd
        if record.polling_place_id == "14258":
            record = record._replace(polling_place_easting="419480")
            record = record._replace(polling_place_northing="422649")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094118631",  # 6 HAND BANK LANE, LOWER HOPTON, MIRFIELD
            "83192424",  # 54 WILDSPUR MILLS, NEW MILL, HOLMFIRTH
            "83192423",  # 53 WILDSPUR MILLS, NEW MILL, HOLMFIRTH
            "83192420",  # 50 WILDSPUR MILLS, NEW MILL, HOLMFIRTH
            "83192421",  # 51 WILDSPUR MILLS, NEW MILL, HOLMFIRTH
            "83192422",  # 52 WILDSPUR MILLS, NEW MILL, HOLMFIRTH
        ]:
            return None

        if record.addressline6 in [
            "WF15 6NP",
            "HD7 6DU",
            "HD7 4NN",
            "HD7 5XB",
            "HD7 4DJ",
            "HD9 7EH",
        ]:
            return None

        return super().address_record_to_dict(record)
