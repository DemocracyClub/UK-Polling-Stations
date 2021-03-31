from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWA"
    addresses_name = "2021-04-08T09:24:44.681755/polling_station_export-2021-04-06.csv"
    stations_name = "2021-04-08T09:24:44.681755/polling_station_export-2021-04-06.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10010059192",  # CARAVAN 81 BURROWS CARAVAN SITE A4118 FROM JUNCTION WITH PORT EYNON BUS TURNING CIRCLE TO JUNCTION WITH CLASSIFIED SECTION B4247, PORT EYNON, SWANSEA
            "10010038594",  # THE FARMHOUSE, CEFN GORWYDD FAWR, GOWERTON, SWANSEA
            "10010041547",  # FLAT, 9 HIGH STREET, GORSEINON, SWANSEA
            "10011729497",  # FLAT THE MARY DILLWYN FFORDD CYNORE, FFORESTFACH, SWANSEA
            "10010059620",  # PENTRE COTTAGE, PENTRE ROAD, PONTARDDULAIS, SWANSEA
            "10010043604",  # CARAVAN CWMDULAIS FARM UNCLASSIFIED SECTION-Y920, PONTARDDULAIS, SWANSEA
            "100101045973",  # FIRST FLOOR FLAT 4 WALTER ROAD, CITY CENTRE, SWANSEA
            "10010035134",  # FLAT 1 141 TERRACE ROAD, MOUNT PLEASANT, SWANSEA
            "100100360550",  # FLAT 2 141 TERRACE ROAD, MOUNT PLEASANT, SWANSEA
            "100100360551",  # FLAT 3 141 TERRACE ROAD, MOUNT PLEASANT, SWANSEA
            "10010037937",  # MAISONETTE FLAT - BOTTOM FLAT 143 TERRACE ROAD, MOUNT PLEASANT, SWANSEA
            "100100360552",  # FIRST FLOOR FLAT TOP FLAT 143 TERRACE ROAD, MOUNT PLEASANT, SWANSEA
            "10010059308",  # CARAVAN EAST MOOR B4247 FROM HILL VIEW TO KIMLEY MOOR FARM, RHOSSILI, SWANSEA
            "10010045307",  # THE NATIONAL TRUST, THE OLD RECTORY UNCLASSIFIED SECTION-Y2402, RHOSSILI, SWANSEA
            "10010059384",  # COTTAGE AT ROBINS NEST UNCLASSIFIED SECTION-Y2085, PENMAEN, SWANSEA
        ]:
            return None

        if record.housepostcode in [
            "SA5 4NN",
            "SA4 3QX",
            "SA6 5JS",
            "SA5 7PH",
            "SA5 7DR",
            "SA5 7HY",
            "SA6 6BW",
            "SA1 8PN",
            "SA3 1AS",
            "SA3 3JS",
            "SA3 4QE",
            "SA1 6NQ",
            "SA6 6QA",
            "SA1 6JP",
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
