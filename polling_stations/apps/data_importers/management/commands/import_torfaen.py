from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "TOF"
    addresses_name = "2026-05-07/2026-02-25T14:25:31.091273/Democracy Club - Idox_2026-02-16 14-22.csv"
    stations_name = "2026-05-07/2026-02-25T14:25:31.091273/Democracy Club - Idox_2026-02-16 14-22.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
            "10013477141",  # GELLI FAWR FARM, HENLLYS, CWMBRAN
        ]:
            return None

        if record.postcode.strip() in [
            # split
            "NP44 5AB",
            "NP4 8LG",
            "NP4 7NW",
            # suspect
            "NP4 8QP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removing bad coords for:
        # BLAENAVON ACTIVE LIVING CENTRE, MIDDLE COED CAE ROAD, BLAENAVON, TORFAEN NP4 9AW
        if self.get_station_hash(record) == "1-blaenavon-active-living-centre":
            record = record._replace(
                pollingvenueeasting="0",
                pollingvenuenorthing="0",
            )
        return super().station_record_to_dict(record)
