from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CMN"
    addresses_name = "2026-05-07/2026-02-17T17:11:18.875080/Democracy Club - Idox_2026-02-17 17-03.csv"
    stations_name = "2026-05-07/2026-02-17T17:11:18.875080/Democracy Club - Idox_2026-02-17 17-03.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        record = record._replace(pollingvenueuprn="")
        # Venue address correction from council for:
        # BLACK MOUNTAIN CENTRE, BRYNAMMAN, CWMGARW ROAD, CANOLFAN Y MYNYDD DU, BRYNAMAN SA18 1BU
        if record.pollingvenueid == "119":
            record = record._replace(
                pollingstationaddress4="HEOL CWMGARW",
                pollingstationaddress5="BRYNAMAN",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10004882480",  # PENYRHEOLWEN, TALLEY, LLANDEILO
            "10009546779",  # PENGOILAN, BETHLEHEM, LLANDEILO
            "10004853865",  # FLAT 1, 3 STATION ROAD, LLANELLI
            "10004848463",  # MERRY VALE, HALFPENNY FURZE, LAUGHARNE, CARMARTHEN
            "10009164875",  # COOMB LODGE, LLANYBRI, CARMARTHEN
        ]:
            return None

        if record.postcode in [
            # split
            "SA14 8BZ",
            "SA16 0LE",
            "SA18 2TA",
            "SA44 5YB",
            "SA17 4NF",
            "SA31 3JJ",
            "SA39 9EU",
            "SA19 8BR",
            "SA14 8TP",
            "SA14 8JA",
            "SA19 8TA",
            "SA15 1HP",
            "SA16 0PP",
            "SA14 8AY",
            "SA15 5LP",
            "SA32 7AS",
            "SA34 0HX",
            "SA18 3DZ",
            "SA20 0EY",
            "SA39 9EJ",
            "SA32 7QJ",
            "SA19 7SG",
            "SA18 3NB",
            "SA19 9AS",
            "SA19 7YE",
            "SA17 5US",
            # suspect
            "SA15 1JE",
        ]:
            return None

        return super().address_record_to_dict(record)
