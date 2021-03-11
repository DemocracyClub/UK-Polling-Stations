from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = "2021-03-10T21:36:45.258417/IOW Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-10T21:36:45.258417/IOW Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060763282",  # 28A HIGH STREET, RYDE
        ]:
            return None

        if record.addressline6 in [
            "PO33 2BP",
            "PO30 5GT",
            "PO36 9NQ",
            "PO30 2DH",
            "PO34 5AF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Annex St Johns Church St. Johns Crescent Sandown PO36 9EQ
        if record.polling_place_id == "7140":
            record = record._replace(polling_place_postcode="PO36 8EQ")

        # Chillerton Village Hall Chillerton Newport
        if record.polling_place_id == "7024":
            record = record._replace(polling_place_postcode="PO30 3ER")

        return super().station_record_to_dict(record)
