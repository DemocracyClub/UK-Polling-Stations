from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = (
        "2024-07-04/2024-06-04T09:33:44.379451/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T09:33:44.379451/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # suspect
            "CO15 1HW",
            "CO15 3BN",
            "CO15 1JG",
            "CO15 1JL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # dirty workaround to remove 32 Colchester stations with no addresses assigned
        # these records are ordered, we can just exclude them by station_code
        if int(record.stationcode) > 77:
            return None
        # station change from council:
        # old: The 1912 Centre, Kings Quay Street, Harwich, Essex CO12 3ES
        # new: Temporary Unit, Wellington road car park, Wellington road, Harwich, Essex, CO12 3DL
        if record.stationcode == "66":
            record = record._replace(
                add1="Wellington Road Car Park",
                add2="Harwich",
                placename="Temporary Unit",
                pollingplaceid="53",
                postcode="CO12 3DL",
                xordinate="",
                yordinate="",
            )
        return super().station_record_to_dict(record)
