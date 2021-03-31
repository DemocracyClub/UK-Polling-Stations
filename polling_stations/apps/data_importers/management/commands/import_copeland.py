from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "COP"
    addresses_name = "2021-03-15T11:52:14.388522/polling_station_export-2021-03-15.csv"
    stations_name = "2021-03-15T11:52:14.388522/polling_station_export-2021-03-15.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "CA25 5JE",
            "CA28 7QS",
            "CA28 6TU",
            "CA19 1UU",
            "CA25 5LN",
            "CA25 5LH",
            "CA22 2TD",
            "CA28 6AQ",
        ]:
            return None

        if uprn in [
            "10000899045",  # STABLE COTTAGE, STEEL GREEN, MILLOM
            "10000897322",  # STEEL GREEN HOUSE, STEEL GREEN, MILLOM
            "10000906979",  # FLAT AT HERDWICKS STEEL GREEN, MILLOM
            "10000898773",  # LANGLEY FARM, BOOTLE, MILLOM
            "10000890830",  # FLOSH FARM CLEATOR, CLEATOR
            "10000901390",  # FURNACE COTTAGE, DUDDON BRIDGE, BROUGHTON-IN-FURNESS
        ]:
            return None

        return super().address_record_to_dict(record)
