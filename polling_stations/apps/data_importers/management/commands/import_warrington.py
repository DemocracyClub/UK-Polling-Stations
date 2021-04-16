from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WRT"
    addresses_name = (
        "2021-03-12T13:29:25.271939/Democracy Club - Polling Districts 2021.csv"
    )
    stations_name = (
        "2021-03-12T13:29:25.271939/Democracy Club - Polling Stations 2021.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # correction from council
        if record.stationcode in ["138", "139"]:
            record = record._replace(add1="Ellesmere Road")
            record = record._replace(postcode="WA4 6DS")

        # Correction from Council
        # Rixton with Glazebrook Community Hall -> St Helen Church
        if record.stationcode == "55":
            record = record._replace(
                add1="Church House",
                add2="Manchester Road",
                add3="Hollinfare",
                add4="Rixton with Glazebrook",
                add5="",
                add6="",
                postcode="WA3 6LB",
                xordinate="",
                yordinate="",
                placename="St Helen Church",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in ["WA4 5PQ", "WA4 1UN"]:
            return None
        if record.uprn in ["200000979589"]:
            return None
        return super().address_record_to_dict(record)
