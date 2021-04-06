from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GLG"
    addresses_name = (
        "2021-04-08T12:32:22.361894/Glasgow_polling_station_export-2021-04-05.csv"
    )
    stations_name = (
        "2021-04-08T12:32:22.361894/Glasgow_polling_station_export-2021-04-05.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "906700157851",  # 2 ELDERPARK STREET, GLASGOW
            "906700436864",  # 0/1 10 ELDERPARK STREET, GLASGOW
            "906700436865",  # 0/2 10 ELDERPARK STREET, GLASGOW
            "906700436866",  # 1/1 10 ELDERPARK STREET, GLASGOW
            "906700436867",  # 1/2 10 ELDERPARK STREET, GLASGOW
            "906700436868",  # 2/1 10 ELDERPARK STREET, GLASGOW
            "906700436869",  # 2/2 10 ELDERPARK STREET, GLASGOW
            "906700436870",  # 3/1 10 ELDERPARK STREET, GLASGOW
            "906700436871",  # 3/2 10 ELDERPARK STREET, GLASGOW
            "906700436872",  # 4/1 10 ELDERPARK STREET, GLASGOW
            "906700436873",  # 4/2 10 ELDERPARK STREET, GLASGOW
            "906700221720",  # 6 ST. JOHNS ROAD, GLASGOW
            "906700306076",  # 0/2 141 THORNLIEBANK ROAD, GLASGOW
            "906700433663",  # 0/1 141 THORNLIEBANK ROAD, GLASGOW
            "906700415121",  # SITE 5 CARAVAN PARK 64 STRATHCLYDE STREET, GLASGOW
        ]:
            return None

        if record.housepostcode in [
            "G61 1QE",
            "G14 9HQ",
            "G52 1RZ",
            "G22 6RL",
            "G21 2LN",
            "G21 4UH",
            "G53 6UW",
            "G33 3SU",
            "G51 2WU",
            "G51 2YJ",
            "G51 2WX",
            "G5 9HR",
            "G5 9HU",
            "G41 5DW",
            "G45 9NH",
            "G15 8JY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if "LINTHAUGH NURSERY" in record.pollingstationname:
            record = record._replace(
                pollingstationpostcode=record.pollingstationaddress_5
            )
            record = record._replace(pollingstationaddress_5="")

        if "CARNTYNE PARISH CHURCH HALL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        if "CARNTYNE PRIMARY SCHOOL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        if "ST MUNGO'S PRIMARY SCHOOL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        if "ST MARGARETS PARISH CHURCH HALL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
