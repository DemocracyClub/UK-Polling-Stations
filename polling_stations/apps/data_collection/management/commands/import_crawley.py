from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000226"
    addresses_name = "2020-02-04T10:49:54.706223/Democracy_Club__07May2020craw.tsv"
    stations_name = "2020-02-04T10:49:54.706223/Democracy_Club__07May2020craw.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline1 == "7B Crawley Foyer":
            rec["postcode"] == "RH11 7AU"

        if uprn in [
            "10024122201"  # RH110EA -> RH110AE : 50A Ifield Drive, Ifield, Crawley
        ]:
            rec["accept_suggestion"] = True

        return rec

    def get_station_point(self, record):

        # Furnace Green Community Centre
        if record.polling_place_id == "910":
            record = record._replace(polling_place_easting="528414")
            record = record._replace(polling_place_northing="135782")

        # Wakehams Green Community Centre
        if record.polling_place_id == "892":
            record = record._replace(polling_place_easting="529968")
            record = record._replace(polling_place_northing="138172")

        # Southgate West Community Centre
        if record.polling_place_id == "898":
            record = record._replace(polling_place_easting="526307")
            record = record._replace(polling_place_northing="135610")

        return super().get_station_point(record)
