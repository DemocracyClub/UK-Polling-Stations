from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWA"
    addresses_name = (
        "2022-05-05/2022-03-03T11:41:12.072581/polling_station_export-2022-03-03.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-03T11:41:12.072581/polling_station_export-2022-03-03.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091617114",  # 5 DUNVANT PARK HOUSES, DUNVANT, SWANSEA, SA2 7SH
            "10010061246",  # SWANSEA & BRECON DIOCESAN BOARD, 1-3 BEACONS VIEW ROAD, CLASE, SWANSEA, SA6 7HJ
            "10010037747",  # FIRST FLOOR FLAT ABOVE YATES 1-4 CAER STREET, CITY CENTRE, SWANSEA, SA1 3PP
            "10094784277",  # ROOM A 116 OLDWAY CENTRE 39 HIGH STREET, CITY CENTRE, SWANSEA, SA1 1LD
            "100100401496",  # 37A HIGH STREET, GORSEINON, SWANSEA, SA4 4BT
            "10011729995",  # ROSE COTTAGE UNCLASSIFIED SECTION-Y2117, OXWICH, SWANSEA, SA3 1LN
            "10010058515",  # THE LAUNDRY MIDDLETON HALL UNCLASSIFIED SECTION-Y2400, RHOSSILI, SWANSEA,SA3 1PJ
        ]:
            return None

        if record.housepostcode in [
            "SA1 8PN",
            "SA5 7HY",
            "SA1 3LQ",
            "SA1 6NQ",
            "SA3 1AS",
            "SA5 7DR",
            "SA3 1BX",
            "SA3 4QE",
            "SA6 6BW",
            "SA6 5JS",
            "SA6 6DS",
            "SA5 4NN",
            "SA3 3JS",
            "SA5 7PH",
            "SA4 3QX",
            "SA1 7GE",
            "SA2 0EU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Llangyfelach Church Hall Swansea Road Llangyfelach Swansea
        if (record.pollingstationnumber, record.pollingstationname) == (
            "7",
            "Llangyfelach Church Hall",
        ):
            record = record._replace(pollingstationpostcode="SA5 7JD")

        return super().station_record_to_dict(record)
