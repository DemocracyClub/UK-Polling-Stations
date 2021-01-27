from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAC"
    addresses_name = "2021-01-22T12:23:53.522413/Democracy_Club__06May2021.CSV"
    stations_name = "2021-01-22T12:23:53.522413/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.polling_place_id == "1504":
            record = record._replace(polling_place_easting="507211")
            record = record._replace(polling_place_northing="204366")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093316891",  # 82 LANCASTER HOUSE FROGMORE ROAD, HEMEL HEMPSTEAD
            "10093316895",  # 78 LANCASTER HOUSE FROGMORE ROAD, HEMEL HEMPSTEAD
            "200004058405",  # WHITEHOUSE GREEN LANE, FLAMSTEAD - NB Avoids confusion with "100081154056 - WHITE HOUSE, GREEN LANE, MARKYATE, ST. ALBANS"
        ]:
            return None

        return rec
