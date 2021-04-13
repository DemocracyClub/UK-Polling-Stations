from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = "2021-04-12T12:33:03.476596/GLA Ealing Polling Station List - Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-12T12:33:03.476596/GLA Ealing Polling Station List - Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "12179425",  # 231B ALLENBY ROAD, SOUTHALL
            "12153714",  # FLAT AT 94 ST MARYS ROAD, EALING
            "12000529",  # TOP LOCK COTTAGE, HAVELOCK ROAD, SOUTHALL
            "12182977",  # 422 GREENFORD ROAD, GREENFORD
        ]:
            return None

        if record.addressline6 in [
            "W4 1DR",
            "W3 8QA",
            "W5 5QX",
            "W5 2JH",
            "UB6 9RZ",
            "UB5 6AT",
            "UB5 5AB",
            "UB2 4PN",
            "UB2 4JR",
            "UB2 5ET",
            "W3 8SZ",
            "UB1 2JP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "5377",  # Temporary Polling Place St Augustine`s Avenue W5
            "5563",  # Temporary Polling Place Blenheim Road Northolt UB5
            "5639",  # Temporary Polling Place Chilton Avenue London W5
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
