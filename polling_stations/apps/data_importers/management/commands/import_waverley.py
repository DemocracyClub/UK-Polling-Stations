from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAE"
    addresses_name = "2021-03-01T10:16:29.232903/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-01T10:16:29.232903/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061614139",  # KINGSLEY, CATTESHALL LANE, GODALMING
            "200001293683",  # 1 GREEN LANE VILLAS, GREEN LANE, CHURT, FARNHAM
            "100061610563",  # 75 UPPER HALE ROAD, FARNHAM
        ]:
            return None

        if record.addressline6 in [
            "GU9 9JT",
            "GU9 0HR",
            "GU10 2JT",
            "GU8 4BH",
            "GU7 3LG",
            "GU7 1LN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Clock Barn Hall, Clock Barn Farm, Hambledon Road, Busbrudge, Godalming
        if record.polling_place_id == "4959":
            record = record._replace(polling_place_address_3="Busbridge")

        return super().station_record_to_dict(record)
