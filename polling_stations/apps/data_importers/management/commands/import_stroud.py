from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STO"
    addresses_name = "2021-04-19T13:57:28.472090/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-19T13:57:28.472090/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Arthur S Winterbotham Memorial Hall High Street Cam
        if record.polling_place_id == "17930":
            record = record._replace(polling_place_easting="374915")
            record = record._replace(polling_place_northing="200440")

        # Bussage Village Hall Bussage Stroud
        if record.polling_place_id == "18022":
            record = record._replace(polling_place_postcode="GL6 8BB")
            record = record._replace(polling_place_easting="388393")
            record = record._replace(polling_place_northing="203373")

        # Rodborough Tabernacle United Reformed Church Tabernacle Walk Rodborough Stroud GL5 3JJ
        if record.polling_place_id == "18181":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003108372",  # 5 WORKMANS CLOSE, DURSLEY
            "100120525233",  # THE FORMER TELEPHONE EXCHANGE, BATH ROAD, HARDWICKE, GLOUCESTER
        ]:
            return None

        if record.post_code in [
            "GL13 9JL",
            "GL5 4NY",
            "GL5 3JL",
            "GL5 1RG",
            "GL2 7NJ",
            "GL5 3JN",
            "GL10 3BN",
            "GL6 9AH",
        ]:
            return None

        return super().address_record_to_dict(record)
