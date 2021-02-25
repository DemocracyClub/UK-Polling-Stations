from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENO"
    addresses_name = "2021-02-18T16:04:59.003549/Democracy_Club__06May2021.tsv"
    stations_name = "2021-02-18T16:04:59.003549/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093005561"  # MOONBEAM WOODFORD RIVERSIDE MARINA ADDINGTON ROAD, WOODFORD
        ]:
            return None

        if record.addressline6 in ["NN9 5UF", "NN14 3BY", "NN10 9JD", "NN10 9NJ"]:
            return None

        return rec

    def station_record_to_dict(self, record):
        # The Albert Underwood Room, St Peters Church, Church Street, Irthlingborough, Wellingborough
        if record.polling_place_id == "10161":
            record = record._replace(polling_place_postcode="")
        return super().station_record_to_dict(record)
