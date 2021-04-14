from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDU"
    addresses_name = "2021-03-22T09:26:21.784038/polling_station_export-2021-03-21.csv"
    stations_name = "2021-03-22T09:26:21.784038/polling_station_export-2021-03-21.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def get_stations(self):
        stations = super().get_stations()
        stations = [
            record for record in stations if record.streetname != "OTHER ELECTORS"
        ]
        return stations

    def get_addresses(self):
        addresses = super().get_stations()
        addresses = [
            record for record in addresses if record.streetname != "OTHER ELECTORS"
        ]
        return addresses

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "132016488",  # WINDYKNOWE COTTAGE, STATION ROAD, LENNOXTOWN, GLASGOW
            "132043041",  # BRAES O YETTS FARM, KIRKINTILLOCH, GLASGOW
            "132023751",  # 4 LENZIE ROAD, KIRKINTILLOCH, GLASGOW
            "132023752",  # 6 LENZIE ROAD, KIRKINTILLOCH, GLASGOW
            "132023979",  # PARKVIEW, LENZIE ROAD, KIRKINTILLOCH, GLASGOW
            "132023978",  # KIRROUGHTREE, LENZIE ROAD, KIRKINTILLOCH, GLASGOW
            "132008358",  # ORCHARDLEA, TORRANCE, GLASGOW
            "132007850",  # 145 BALMUILDY ROAD, BISHOPBRIGGS, GLASGOW
            "132008282",  # HILTON COTTAGE, BALMUILDY ROAD, BISHOPBRIGGS, GLASGOW
            "132008265",  # HILTON FARM COTTAGE, BALMUILDY ROAD, BISHOPBRIGGS, GLASGOW
            "132001702",  # 129 MILNGAVIE ROAD, BEARSDEN, GLASGOW
        ]:
            return None

        if record.housepostcode in [
            "G66 7HE",
            "G66 7HL",
            "G66 7AS",
            "G64 2DF",
            "G64 4DQ",
            "G66 4QH",
            "G64 1FR",
            "G61 1RS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.adminarea not in [
            "EAST DUNBARTONSHIRE",
            "GLASGOW",
        ] and record.pollingstationname not in [
            "HILLHEAD COMMUNITY CENTRE",
            "LENNOXTOWN PRIMARY SCHOOL",
        ]:
            return None
        return super().station_record_to_dict(record)
