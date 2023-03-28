from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HOR"
    addresses_name = (
        "2023-05-04/2023-03-28T17:03:47.545526/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-28T17:03:47.545526/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096224629",  # 11 GREENFIELD FARM, VALEWOOD LANE, BARNS GREEN, HORSHAM
            "10013788049",  # 1 FAIRMEAD, HIGH STREET, BILLINGSHURST
            "10013788050",  # 2 FAIRMEAD, HIGH STREET, BILLINGSHURST
            "10013788051",  # 3 FAIRMEAD, HIGH STREET, BILLINGSHURST
            "10094145111",  # AMARI, ROCK ROAD, STORRINGTON, PULBOROUGH
            "100061814530",  # TWO ACRES, LANGHURSTWOOD ROAD, HORSHAM
            "200004786681",  # WOODLANDS CHASE, SEDGWICK LANE, HORSHAM
            "200004781030",  # HORSEBROOK COTTAGE, STEYNING ROAD, WISTON, STEYNING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RH13 9JP",
            "RH13 0NB",
            "RH12 2ES",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Billingshurst Centre, Roman Way, Billingshurst, RH14 9QW
        if record.polling_place_id == "3817":
            record = record._replace(
                polling_place_easting="508896",
                polling_place_northing="126249",
            )

        # Ravenscroft Guide & Community Centre, Browns Lane, Storrington, RH20 4LQ
        if record.polling_place_id == "3766":
            record = record._replace(
                polling_place_easting="508805",
                polling_place_northing="114119",
            )

        # Thakeham Village Hall, 1 Abingworth Crescent, Thakeham, RH20 3GW
        if record.polling_place_id == "3797":
            record = record._replace(
                polling_place_easting="510436",
                polling_place_northing="116834",
            )
        return super().station_record_to_dict(record)
