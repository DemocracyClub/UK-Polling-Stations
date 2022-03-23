from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = (
        "2022-05-05/2022-03-23T16:21:32.597129/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:21:32.597129/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"


def address_record_to_dict(self, record):
    if record.addressline6 in [
        "L23 7TX",
        "L20 6EA",
    ]:
        return None

    return super().address_record_to_dict(record)


def station_record_to_dict(self, record):
    # Bootle Main Library 220 Stanley Road Bootle L20 3GN
    if record.polling_place_id == "8672":
        record = record._replace(polling_place_postcode="")

    return super().station_record_to_dict(record)
