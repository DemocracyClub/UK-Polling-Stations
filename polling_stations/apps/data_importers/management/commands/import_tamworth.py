from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = "2023-05-04/2023-04-25T14:30:27.355270/Tamworth_polling-stations_May _2023_for_Democracy-Club.tsv"
    stations_name = "2023-05-04/2023-04-25T14:30:27.355270/Tamworth_polling-stations_May _2023_for_Democracy-Club.tsv"

    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "394037200",  # 105A COMBERFORD ROAD, TAMWORTH
            "394030964",  # STATFOLD BARN FARM ASHBY ROAD, TAMWORTH
        ]:
            return None
        if record.addressline6 in [
            # splits
            "B77 3EU",
        ]:
            return None

        return super().address_record_to_dict(record)
