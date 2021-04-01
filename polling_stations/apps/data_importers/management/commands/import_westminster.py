from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WSM"
    addresses_name = "2021-03-30T13:02:54.918672/polling_station_export-2021-03-30.csv"
    stations_name = "2021-03-30T13:02:54.918672/polling_station_export-2021-03-30.csv"
    elections = ["2021-05-06"]

    # Have checked "Mornington Hotel 12 Lancaster Gate" and
    # "York Room, Lancaster Hall Hotel 35 Craven Terrace" closeness; all good.

    # These all have wrong locations in AddressBase, but have the right station
    # for their actual location.
    #     "10033552804",  # Flat 3, 2 Moreton Close
    #     "100022803552",  # 9 ST.BARNABAS STREET, LONDON
    #     "100022749688",  # 50 ELNATHAN MEWS, LONDON

    def replace_station_96(self, record):
        # https://trello.com/c/HpRDeeyv/401-westminster
        if record.pollingstationnumber == "96":
            record = record._replace(
                pollingstationaddress_1="Cumberland Street",
                pollingstationaddress_2="London",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationaddress_5="",
                pollingstationname="Holy Apostles Church Hall",
                pollingstationpostcode="SW1V 4LY",
            )
        return record

    def station_record_to_dict(self, record):
        record = self.replace_station_96(record)
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        # This has to be here too, so the station ID is calculated correctly from the
        # name.
        record = self.replace_station_96(record)

        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "NW8 9LJ",
            "W1U 8BD",
            "W2 5HA",
            "SW1P 4JZ",
            "NW8 8LH",
            "W2 2QN",
            "W9 3DW",
            "W9 2AL",
            "W9 1SF",
            "W10 4PR",
        ]:
            return None  # split

        # Carried-over postcode fixes

        if record.houseid == "10010095":  # W9 1DL
            rec["postcode"] = "W9 2DL"

        if uprn == "100022801294":
            rec["postcode"] = "W1J 7JJ"

        if uprn == "100023474073":
            rec["postcode"] = "W1J 6HL"

        if uprn == "10033565232":
            rec["postcode"] = "SW7 5HF"

        if uprn == "10033561131":
            rec["postcode"] = "SW1P 4SA"

        return rec
