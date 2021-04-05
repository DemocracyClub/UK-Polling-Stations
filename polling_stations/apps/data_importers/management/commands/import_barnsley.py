from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = "2021-03-12T14:20:28.775183/Democracy Club Polling Districts.csv"
    stations_name = "2021-03-12T14:20:28.775183/Democracy Club Polling Stations.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # TEMPORARY BUILDING AT GRASMERE CRESCENT
        if record.stationcode == "24A":
            record = record._replace(xordinate="", yordinate="")

        # DARFIELD COMMUNITY CENTRE, DARHAVEN, DARFIELD, BARNSLEY
        if record.stationcode == "15A":
            record = record._replace(xordinate="441313", yordinate="404680")
        #
        return super().station_record_to_dict(record)

    #
    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "2007005952",  # BLUE SLATES COTTAGE BROCKHOLES LANE, CUBLEY, BARNSLEY
            "2007021481",  # 24 REDHAW ROAD, ROYSTON, BARNSLEY
            "2007003887",  # WOOD END, OUGHTIBRIDGE LANE, OUGHTIBRIDGE, SHEFFIELD
            "2007003913",  # HOLMES FARM, MAIN ROAD, WHARNCLIFFE SIDE, SHEFFIELD
        ]:
            return None

        return super().address_record_to_dict(record)
