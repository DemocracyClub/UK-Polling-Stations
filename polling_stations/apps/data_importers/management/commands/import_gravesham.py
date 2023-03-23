from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRA"
    addresses_name = "2023-05-04/2023-02-21T21:14:28.593307/polling-stations-export.csv"
    stations_name = "2023-05-04/2023-02-21T21:14:28.593307/polling-stations-export.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode.strip() in ["ME3 7NB"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingstationnumber in (
            "4",
            "52",
        ):  # Shears Green Community Centre, Shears Green Community Centre, 9 Westcott Avenue, Northfleet, Kent
            record = record._replace(
                pollingstationname="Shears Green Community Centre",
                pollingstationaddress_1="9 Westcott Avenue",
                pollingstationaddress_2="",
            )
        if (
            record.pollingstationnumber == "23"
        ):  # Hive House Library, Hive House, 10-11 The Hive, Northfleet, Kent
            record = record._replace(
                pollingstationname="The Hive Library",
            )
        if (
            record.pollingstationnumber == "7"
        ):  # Riverside Family Learning, Riverside Community Resource Trust, Dickens Road, Gravesend, Kent
            record = record._replace(
                pollingstationname="Riverside Family Learning Centre",
                pollingstationaddress_1="",
            )
        if (
            record.pollingstationnumber == "21"
        ):  # Culverstone Community Hall, Culverstone Community Centre, Whitepost Lane, Culverstone, Meopham, Kent
            record = record._replace(
                pollingstationname="Culverstone Community Centre",
                pollingstationaddress_1="",
            )

        if record.pollingstationname == "WHISSENDINE MEMORIAL HALL":
            record = record._replace(pollingstationpostcode="LE15 7ET")
        if record.pollingstationname == "LANGHAM VILLAGE HALL":
            record = record._replace(pollingstationpostcode="LE15 7JE")

        return super().station_record_to_dict(record)
