from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KET"
    addresses_name = "2021-03-19T15:43:36.348322/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-19T15:43:36.348322/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # United Reformed Church Rooms St Peters Avenue entrance Kettering NN15 6DU
        if record.polling_place_id == "5462":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")
            record = record._replace(polling_place_postcode="NN16 0HA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031081643",  # THE LODGE SUTTON LANE, DINGLEY
            "10007877421",  # CARAVAN 1 DESBOROUGH ROAD, BRAYBROOKE
            "10007863000",  # ANNEXE, WHITEGATES FARM, RUSHTON, KETTERING
            "100032143126",  # STYLES COTTAGE, RUSHTON ROAD, ROTHWELL, KETTERING
            "10007870488",  # 1 GRAFTON ROAD, CRANFORD, KETTERING
            "10094095271",  # 13 THE OLD A43, BROUGHTON
        ]:
            return None

        if record.addressline6 in ["NN16 9QA", "NN16 0RY", "NN14 6AB"]:
            return None

        return super().address_record_to_dict(record)
