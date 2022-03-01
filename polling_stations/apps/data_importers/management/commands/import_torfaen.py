from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TOF"
    addresses_name = (
        "2022-05-05/2022-03-01T07:51:07.153603/polling_station_export-2022-03-01.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-01T07:51:07.153603/polling_station_export-2022-03-01.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
        ]:
            return None

        if record.housepostcode in [
            "NP4 7NW",
            "NP4 8JQ",
            "NP4 8LG",
            "NP44 1LE",
            "NP44 4QS",
            #         "NP4 6TX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # FORGESIDE COMMUNITY CENTRE FORGESIDE COMMUNITY CENTRE BFORGESIDE BLAENAVON TORFAEN NP4 9BD
        if record.pollingstationname == "FORGESIDE COMMUNITY CENTRE":
            record = record._replace(pollingstationpostcode="NP4 9DH")

        # THORNHILL4UTOO THORNHILL COMMUNITY CENTRE LEADON COURT THORNHILL CWMBRAN TORFAEN NP44 5YZ
        if record.pollingstationname == "THORNHILL4UTOO":
            record = record._replace(pollingstationpostcode="NP44 5TZ")

        return super().station_record_to_dict(record)
