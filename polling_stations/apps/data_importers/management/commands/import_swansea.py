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

        # The following stations have postcodes that don't match their postcode in addressbase:
        # These are only off by one letter so I'm commenting them out until the council responds:

        # # 'Bonymaen Community Centre, Bonymaen Road, Bonymaen, Swansea, SA1 7AW' (id: 137)
        # if record.pollingvenueid == '137': record = record._replace(pollingstationpostcode='SA1 7AT')

        # # 'Christ Well United Reformed Church, 124-136 Manselton Road, Manselton, Swansea, SA5 8PW' (id: 101)
        # if record.pollingvenueid == '101': record = record._replace(pollingstationpostcode='SA5 8PZ')

        # # 'Sketty Park Community Centre, Heather Crescent, Sketty, Swansea, SA2 8HE' (id: 66)
        # if record.pollingvenueid == '66': record = record._replace(pollingstationpostcode='SA2 8HS')

        # # 'City Church Swansea, Dyfatty Street, Swansea, SA1 1QG' (id: 89)
        # if record.pollingvenueid == '89': record = record._replace(pollingstationpostcode='SA1 1QQ')

        # # 'Brynmelyn Community Centre, Park Terrace, Brynmelyn, Swansea, SA1 2BY' (id: 92)
        # if record.pollingvenueid == '92': record = record._replace(pollingstationpostcode='SA1 2BZ')

        # # 'Salvation Army, 40 Richardson Street, Swansea, SA1 3TE' (id: 85)
        # if record.pollingvenueid == '85': record = record._replace(pollingstationpostcode='SA1 3TY')

        # These are off by two letters so I'm removing them:

        # 'St. Thomas Church, Lewis Street, St. Thomas, Swansea, SA1 8BP' (id: 138)
        if record.pollingvenueid == "138":
            record = record._replace(pollingstationpostcode="")

        # 'Mobile Station at land next to Lon Claerwen, Caemawr, Morriston, Swansea, SA6 7EQ' (id: 124)
        if record.pollingvenueid == "124":
            record = record._replace(pollingstationpostcode="")

        # 'Swansea Mosque, 159A St Helen's Road, Swansea, SA1 4DQ' (id: 86)
        if record.pollingvenueid == "86":
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
