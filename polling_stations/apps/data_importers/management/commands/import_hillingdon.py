from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = "2021-03-25T09:17:18.067946/Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-25T09:17:18.067946/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Walter G Pomeroy Hall, Royal Lane, Hillingdon
        if record.polling_place_id == "9559":
            record = record._replace(polling_place_easting="506536")
            record = record._replace(polling_place_northing="181610")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021469325",  # 1 ELM VIEW HOUSE, SHEPISTON LANE, HAYES
            "100023417375",  # WESTWAY FARM, CHARVILLE LANE, HAYES
            "100022832219",  # 241 BALMORAL DRIVE, HAYES
            "100021415478",  # 48A THE FAIRWAY, RUISLIP
            "10022802358",  # MANAGERS FLAT BAITUL AMAN MOSQUE ROYAL LANE, UXBRIDGE
            "100021461989",  # MANAGERS FLAT THE GEORGE HARVESTER BURY STREET, RUISLIP
        ]:
            return None

        if record.addressline6 in [
            "UB10 0LF",
            "UB7 9LW",
            "UB3 3PF",
            "UB10 0LE",
            "UB10 8LF",
            "UB8 2YF",
            "UB9 6NA",
            "UB8 2TZ",
            "TW6 2AL",
            "UB8 3DH",
            "UB8 1GW",
            "UB9 6QS",
            "UB3 2FH",
            "UB8 3QD",
            "UB10 0QB",
            "HA4 0SE",
            "HA6 1RL",
        ]:
            return None

        return super().address_record_to_dict(record)
