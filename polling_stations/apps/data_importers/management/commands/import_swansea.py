from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWA"
    addresses_name = "2024-07-04/2024-06-18T11:28:54.964026/SWA_combined.csv"
    stations_name = "2024-07-04/2024-06-18T11:28:54.964026/SWA_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091617114",  # 5 DUNVANT PARK HOUSES, DUNVANT, SWANSEA, SA2 7SH
            "10010037747",  # FIRST FLOOR FLAT ABOVE YATES 1-4 CAER STREET, CITY CENTRE, SWANSEA, SA1 3PP
            "10094784277",  # ROOM A 116 OLDWAY CENTRE 39 HIGH STREET, CITY CENTRE, SWANSEA, SA1 1LD
            "100100401496",  # 37A HIGH STREET, GORSEINON, SWANSEA, SA4 4BT
            "10011729995",  # ROSE COTTAGE UNCLASSIFIED SECTION-Y2117, OXWICH, SWANSEA, SA3 1LN
            "10010058515",  # THE LAUNDRY MIDDLETON HALL UNCLASSIFIED SECTION-Y2400, RHOSSILI, SWANSEA,SA3 1PJ
            "10010046963",  # LLE'R FEDWEN FARM, FELINDRE, SWANSEA
        ]:
            return None

        if record.housepostcode in [
            # split
            "SA6 6DS",
            "SA1 8PN",
            "SA1 6NQ",
            "SA5 7HY",
            "SA4 3QX",
            "SA3 3JS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Llangyfelach Church Hall Swansea Road Llangyfelach Swansea
        if self.get_station_hash(record) == "7-llangyfelach-church-hall":
            record = record._replace(pollingstationpostcode="SA5 7JD")

        # The council has requested that we ignore postcode mismatches for the following stations:

        # 'Bonymaen Community Centre, Bonymaen Road, Bonymaen, Swansea, SA1 7AW' (id: 137)
        # 'Christ Well United Reformed Church, 124-136 Manselton Road, Manselton, Swansea, SA5 8PW' (id: 101)
        # 'Sketty Park Community Centre, Heather Crescent, Sketty, Swansea, SA2 8HE' (id: 66)
        # 'City Church Swansea, Dyfatty Street, Swansea, SA1 1QG' (id: 89)
        # 'Brynmelyn Community Centre, Park Terrace, Brynmelyn, Swansea, SA1 2BY' (id: 92)
        # 'Salvation Army, 40 Richardson Street, Swansea, SA1 3TE' (id: 85)
        # 'St. Thomas Church, Lewis Street, St. Thomas, Swansea, SA1 8BP' (id: 138)
        # 'Mobile Station at land next to Lon Claerwen, Caemawr, Morriston, Swansea, SA6 7EQ' (id: 124)
        # 'Swansea Mosque, 159A St Helen's Road, Swansea, SA1 4DQ' (id: 86)

        return super().station_record_to_dict(record)
