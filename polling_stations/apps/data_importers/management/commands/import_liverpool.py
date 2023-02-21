from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIV"
    addresses_name = "2021-04-20T11:27:13.719847/Liverpool_deduped.csv"
    stations_name = "2021-04-20T11:27:13.719847/Liverpool_deduped.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "38318034",  # 3A ALLERTON ROAD, WOOLTON, LIVERPOOL
            "38241263",  # FLAT 1A 13 DEVONSHIRE ROAD, LIVERPOOL
        ]:
            return None

        if record.addressline6 in ["L16 1JH", "L11 4TD", "L14 3LF"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "8365",  # St.Mary`s Church Parish Hall, St Mary`s Road, Liverpool L19 0PW
            "8485",  # Temporary Polling Station, Opposite 2 Lingfield Road, Near Its Junction With, Thomas Drive, Liverpool L14
            "8723",  # Temporary Polling Station, Coachmans Drive, Liverpool L12
            "8330",  # Temporary Polling Station, Broadway Nursing Home, Flemington Avenue, Liverpool L4
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
