from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCC"
    addresses_name = "2021-03-10T11:51:24.840947/Redcar Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-10T11:51:24.840947/Redcar Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034524783",  # SCHOOL HOUSE, STATION LANE, SKELTON-IN-CLEVELAND, SALTBURN-BY-THE-SEA
        ]:
            return None

        if record.addressline6 in ["TS10 4AJ"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Whale Hill Community Centre Goathland Road Whale Hill Estate Eston TS6 8EW
        if record.polling_place_id == "15850":
            record = record._replace(polling_place_postcode="TS6 8AW")

        return super().station_record_to_dict(record)
