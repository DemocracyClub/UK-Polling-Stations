from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SEL"
    addresses_name = (
        "2023-07-20/2023-06-26T14:06:22/Selby & Ainsty_Democracy_Club__20July2023.CSV"
    )
    stations_name = (
        "2023-07-20/2023-06-26T14:06:22/Selby & Ainsty_Democracy_Club__20July2023.CSV"
    )
    elections = ["2023-07-20"]

    selby_stations = [
        "56296",
        "56305",
        "56309",
        "56313",
        "56317",
        "56321",
        "56324",
        "56328",
        "56331",
        "56335",
        "56338",
        "56342",
        "56346",
        "56350",
        "56354",
        "56358",
        "56362",
        "56365",
        "56369",
        "56372",
        "56376",
        "56380",
        "56383",
        "56386",
        "56390",
        "56394",
        "56397",
        "56401",
        "56405",
        "56409",
        "56413",
        "56527",
        "56421",
        "56427",
        "56431",
        "56432",
        "56435",
        "56438",
        "56442",
        "56446",
        "56450",
        "56454",
        "56457",
        "56458",
        "56461",
        "56514",
        "56462",
        "56467",
        "56471",
        "56474",
        "56478",
        "56482",
        "56484",
        "56483",
        "56488",
        "56490",
        "56494",
        "56498",
        "56502",
        "56523",
        "56509",
    ]

    def station_record_to_dict(self, record):
        if record.polling_place_id not in self.selby_stations:
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.polling_place_id not in self.selby_stations:
            return None

        if record.addressline6 in [
            "YO8 8FH",
            "LS24 9HH",
        ]:
            return None
        return super().address_record_to_dict(record)
