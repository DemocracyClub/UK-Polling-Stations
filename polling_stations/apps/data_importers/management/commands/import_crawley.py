from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = "2021-03-19T10:25:17.143451/Crawley Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-19T10:25:17.143451/Crawley Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Furnace Green Community Centre
        if record.polling_place_id == "968":
            record = record._replace(polling_place_easting="528414")
            record = record._replace(polling_place_northing="135782")

        # Wakehams Green Community Centre
        if record.polling_place_id == "983":
            record = record._replace(polling_place_easting="529968")
            record = record._replace(polling_place_northing="138172")

        # Southgate West Community Centre
        if record.polling_place_id == "989":
            record = record._replace(polling_place_easting="526307")
            record = record._replace(polling_place_northing="135610")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001224606",  # CARETAKER FLAT TA CENTRE 29 KILNMEAD, NORTHGATE, CRAWLEY
        ]:
            return None

        if record.addressline6 in ["RH10 7AU"]:
            return None

        return super().address_record_to_dict(record)
