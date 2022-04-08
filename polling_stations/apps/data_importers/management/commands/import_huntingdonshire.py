from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = (
        "2022-05-05/2022-04-08T13:56:19.938577/UPDATED Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-08T13:56:19.938577/UPDATED Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091593436",  # 26D ALEXANDRA HOUSE HINCHINGBROOKE HOSPITAL HINCHINGBROOKE PARK ROAD, HUNTINGDON
        ]:
            return None

        if record.addressline6 in [
            "PE19 1HW",
            "PE27 6DT",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Berkley Street Methodist Church, Berkley Street, Eynesbury, St. Neots, PE19 2HD
        if record.polling_place_id == "8397":
            record = record._replace(polling_place_postcode="PE19 2NB")

        return super().station_record_to_dict(record)
