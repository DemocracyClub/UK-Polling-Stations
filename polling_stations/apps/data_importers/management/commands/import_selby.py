from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SEL"
    addresses_name = "2021-03-16T14:34:21.177117/Democracy_Club__06May2021 (1).tsv"
    stations_name = "2021-03-16T14:34:21.177117/Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001023825",  # WILLOW FARM, DONCASTER ROAD, TADCASTER
            "200001017730",  # WHITEMOOR GRANGE WHITEMOOR LANE, BARLBY, SELBY
        ]:
            return None

        if record.addressline6 in ["YO8 8FH", "YO8 3EH", "LS24 9HH", "YO8 3ED"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Selby Rugby Club Sandhill Lane Selby YO8 4HP
        if record.polling_place_id == "6168":
            record = record._replace(polling_place_postcode="YO8 4JP")

        # Lady Popplewell Centre Beechwood Close Sherburn in Elmet Leeds LS25 6HO
        if record.polling_place_id == "6162":
            record = record._replace(polling_place_postcode="LS25 6HU")

        return super().station_record_to_dict(record)
