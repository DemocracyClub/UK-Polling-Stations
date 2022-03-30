from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "COP"
    addresses_name = (
        "2022-05-05/2022-03-30T12:34:42.381612/polling_station_export-2022-03-16.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-30T12:34:42.381612/polling_station_export-2022-03-16.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "CA19 1UU",
            "CA25 5JE",
            "CA22 2TD",
            "LA19 5XT",
            "CA28 7QS",
            "CA28 6TU",
        ]:
            return None  # split

        if uprn in [
            "10000899045",  # STABLE COTTAGE, STEEL GREEN, MILLOM
            "10000897322",  # STEEL GREEN HOUSE, STEEL GREEN, MILLOM
            "10000906979",  # FLAT AT HERDWICKS STEEL GREEN, MILLOM
            "10000898773",  # LANGLEY FARM, BOOTLE, MILLOM
            "10000890830",  # FLOSH FARM CLEATOR, CLEATOR
        ]:
            return None

        return super().address_record_to_dict(record)
