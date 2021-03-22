from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2021-03-05T10:59:45.248759/polling_station_export-2021-03-04.csv"
    stations_name = "2021-03-05T10:59:45.248759/polling_station_export-2021-03-04.csv"
    elections = ["2021-05-06"]

    # Note: these warning has been checked and all looks fine.
    # > WARNING: Polling stations 'Welton Vale Community Room 9 Welton Vale' and
    # > 'The Salvation Army Radstock Road / Stones Cross' are at approximately the same
    # > location
    #
    # The centroid is outside, but the polling place is within.
    # > WARNING: Polling station 85-prattens-westfield-amateur-sports-club is in Mendip
    # > District Council (MEN) but target council is Bath & North East Somerset Council
    # > (BAS) - manual check recommended

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in ["BS31 1AJ", "BA2 2RZ", "BA3 4GA", "BS31 1GB"]:
            return None  # split

        if uprn == "10093715348":  # 'O' -> '0'
            record = record._replace(housepostcode="BS14 0FR")

        if record.houseid.strip() == "9002893":  # 'O' -> '0'
            record = record._replace(housepostcode="BA2 0LH")

        rec = super().address_record_to_dict(record)

        # Addressbase has this postcode geolocated in the LA, however ONSPD doesn't.
        # This line is in to squash the
        # "Postcode centroid is outside target local authority" Warnings
        if record.housepostcode == "BA3 5SF":
            return None

        if record.pollingstationnumber == "n/a":
            return None

        return rec
