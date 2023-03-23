from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2023-05-04/2023-04-06T12:57:54.299279/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-06T12:57:54.299279/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Moston Methodist Church corner of Ilkley Street and Moston Lane Moston Manchester
        if record.polling_place_id == "12679":
            record = record._replace(
                polling_place_easting="387244", polling_place_northing="401944"
            )

        # if record.addressline1 in ["NEW POLLING STATION", "CHANGE OF STATION"]:
        #     record = record._replace(addressline1="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "M1 2PE",
            "M8 9AE",
            "M12 5PR",
            "M22 8BE",
            # look wrong
            "M22 5BL",
            "M8 4RB",
        ]:
            return None

        return super().address_record_to_dict(record)
