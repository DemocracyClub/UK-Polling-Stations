from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HEF"
    addresses_name = "2021-02-23T12:40:34.098231/polling_station_export-2021-02-22.csv"
    stations_name = "2021-02-23T12:40:34.098231/polling_station_export-2021-02-22.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093119764",  # TIRBILL, BLACK HILL FARM, LLANVEYNOE, LONGTOWN, HEREFORD
            "10023977670",  # STOCKIN FARM COTTAGE, RICHARDS CASTLE, LUDLOW
            "200002634580",  # SUMMER HILL, HAYNALL LANE, LITTLE HEREFORD, LUDLOW
            "10009581132",  # CRADOC COTTAGE CRADOC COURT PLOCKS COURT, ALLENSMORE
            "10009557901",  # SNOW DROP COVERT, HAYNALL LANE, LITTLE HEREFORD, LUDLOW
            "10009576304",  # GREENWAY AT WOODREDDING FARM A449 FROM HILLINGTON TO WOODREDDING FARM, WOODREDDING
            "10091654013",  # PLOUGHMANS, WOODREDDING, ROSS-ON-WYE
            "10023978747",  # CORNERWAYS KENT AVENUE, ROSS-ON-WYE
            "10009578073",  # CRADOC COURT, ALLENSMORE, HEREFORD
            "10022775876",  # HOME FARM, CROFT, LEOMINSTER
            "10022778892",  # GRYMSTYCH COTTAGE EAST STREET, PEMBRIDGE
            "10022783983",  # THE POPLARS, WIGMORE, LEOMINSTER
            "10009564500",  # PANTEG, YATTON, ROSS-ON-WYE
        ]:
            return None

        if record.housepostcode.strip() in ["HR4 9EN", "HR2 8FH"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council fix
        if record.pollingstationnumber == "21":
            return {
                "internal_council_id": "21-bromyard-public-hall",
                "postcode": "HR7 4EB",
                "address": "Bromyard Public Hall\nRowberry Street\nBromyard",
                "location": None,
            }
        return super().station_record_to_dict(record)
