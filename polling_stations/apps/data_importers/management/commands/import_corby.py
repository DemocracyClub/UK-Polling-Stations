from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COR"
    addresses_name = (
        "2021-02-18T12:24:59.338256/Corby Democracy_Club__06May2021 (1).tsv"
    )
    stations_name = "2021-02-18T12:24:59.338256/Corby Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "NN17 1FP",
            "NN17 2HP",
            "NN18 8DZ",
            "NN18 9BD",
            "NN18 8QG",
            "NN18 8RS",
            "NN18 0LT",
            "NN18 0LT",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):

        if (
            record.polling_place_id == "7919"
        ):  # Stanion Village Hall, Brigstock Road, Stanion, Kettering
            record = record._replace(polling_place_postcode="NN14 1BU")

        if (
            record.polling_place_id == "7971"
        ):  # St Andrew`s Church of Scotland, Church Hall, Occupation Road, Corby
            record = record._replace(polling_place_postcode="NN17 1EB")

        if (
            record.polling_place_id == "7903"
        ):  # Cottingham/Middleton Village Hall, Berryfield Road, Cottingham, Market Harborough
            record = record._replace(polling_place_postcode="LE16 8XB")

        if (
            record.polling_place_id == "7932"
        ):  # The Autumn Centre, Counts Farm Road, Corby
            record = record._replace(polling_place_postcode="NN18 8BH")

        if (
            record.polling_place_id == "7911"
        ):  # East Carlton Cricket Club, East Carlton Park, East Carlton, Market Harborough
            record = record._replace(polling_place_postcode="LE16 8YF")

        if (
            record.polling_place_id == "8004"
        ):  # The Welcome Centre, Roman Road, Corby, NN18 8FZ
            record = record._replace(polling_place_postcode="NN18 8EY")

        return super().station_record_to_dict(record)
