from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAO"
    addresses_name = (
        "2024-07-04/2024-05-28T15:59:47.852056/Democracy_Club__04July2024 R&S.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T15:59:47.852056/Democracy_Club__04July2024 R&S.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094812143",  # 5 LEAS CLOSE, ULLESTHORPE, LUTTERWORTH
            "10002645475",  # 11 HARBOROUGH ROAD, BILLESDON, LEICESTER
            "200003738208",  # LAUNDE ABBEY, LAUNDE ROAD, LAUNDE, LEICESTER
            "10034462037",  # 10 EADY DRIVE, MARKET HARBOROUGH
            "200003741786",  # NEWTON GRANGE, TILTON LANE, BILLESDON, LEICESTER
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Billesdon Coplow Centre, Uppingham Road, Billesdon, Leicester, LE7 9ER
        # source: https://www.thecoplowcentre.com/contact
        if record.polling_place_id == "7853":
            record = record._replace(polling_place_postcode="LE7 9FL")

        return super().station_record_to_dict(record)
