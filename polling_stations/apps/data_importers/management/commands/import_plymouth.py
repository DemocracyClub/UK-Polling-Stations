from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = (
        "2022-05-05/2022-03-31T10:39:45.450211/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-31T10:39:45.450211/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Chaddlewood Farm Community Centre 80 Chaddlewood District Centre Glen Road Plympton Plymouth PL7 2XS
        if record.polling_place_id == "5916":
            record = record._replace(polling_place_easting="256137")
            record = record._replace(polling_place_northing="56152")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070771403",
            "10070771404",
            "100040493091",
            "100040429061",
        ]:
            return None

        if record.addressline6 in [
            "PL3 6EP",
            "PL4 7QB",
            "PL6 5JZ",
        ]:
            return None

        return super().address_record_to_dict(record)
