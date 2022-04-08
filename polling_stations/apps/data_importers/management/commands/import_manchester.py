from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2022-05-05/2022-03-24T10:46:00.928091/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T10:46:00.928091/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Moston Methodist Church corner of Ilkley Street and Moston Lane Moston Manchester
        if record.polling_place_id == "9372":
            record = record._replace(
                polling_place_easting="387244", polling_place_northing="401944"
            )

        if record.addressline1 in ["NEW POLLING STATION", "CHANGE OF STATION"]:
            record = record._replace(addressline1="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "M8 9AE",
            "M1 2PE",
            "M12 5PR",
            "M8 4RB",
            "M22 8BE",
        ]:
            return None

        return super().address_record_to_dict(record)
