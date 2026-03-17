from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "LEE"
    addresses_name = "2026-05-07/2026-03-17T15:52:41.578389/Democracy Club - Idox_2026-03-17 15-46.csv"
    stations_name = "2026-05-07/2026-03-17T15:52:41.578389/Democracy Club - Idox_2026-03-17 15-46.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10033272374",  # 24A STEYNING AVENUE, PEACEHAVEN
                "200001466148",  # OLD WHEEL COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
                "100062487484",  # WOODS COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
            ]
        ):
            return None

        if record.postcode in [
            # split
            "BN10 8UG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station ST MARTINS CHURCH HALL (54-st-martins-church-hall) is in Brighton and Hove Council (BNH)
        # location is correct

        # location override for: ST MARYS SOCIAL CENTRE CHRISTIE ROAD LEWES, BN7 1PL
        # geocoding from postcode is correct
        if record.pollingstationnumber == "9":
            record = record._replace(pollingvenueeasting="0", pollingvenuenorthing="0")

        return super().station_record_to_dict(record)
