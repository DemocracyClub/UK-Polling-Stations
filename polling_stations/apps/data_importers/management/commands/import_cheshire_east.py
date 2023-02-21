from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = (
        "2021-03-26T11:36:57.996137/Cheshire East Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-26T11:36:57.996137/Cheshire East Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007957663",  # THE FLAT PARK TAVERN 158 PARK LANE, POYNTON
            "100012369170",  # FLAT HIGHFIELD HOUSE 298 PARK LANE, POYNTON
            "100012596063",  # 2A HENRY STREET, HASLINGTON
            "200001127574",  # THE SHEILING, DODDINGTON, NANTWICH
            "100012357368",  # MOSS FARM PARKERS ROAD, CREWE
        ]:
            return None

        if record.addressline6 in [
            "SK12 1UB",
            "CW4 7AG",
            "CW2 8LA",
            "CW5 7HN",
            "ST7 2ZN",
            "ST7 2ZT",
            "SK11 7ZG",
            "ST7 2AJ",
            "ST7 2FN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Goodwill Hall Wrexham Road Faddiley Nantwich CW5 8HX
        if record.polling_place_id == "1785":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
