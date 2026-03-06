from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HOR"
    addresses_name = (
        "2026-05-07/2026-03-06T14:33:29.013429/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-06T14:33:29.013429/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10013788049",  # 1 FAIRMEAD, HIGH STREET, BILLINGSHURST
                "10013788050",  # 2 FAIRMEAD, HIGH STREET, BILLINGSHURST
                "10013788051",  # 3 FAIRMEAD, HIGH STREET, BILLINGSHURST
                "200004791435",  # POLECAT MANOR, POLECAT LANE, SOUTHWATER, HORSHAM
                "100061833314",  # DYKE FARM, WEST CHILTINGTON ROAD, PULBOROUGH
                "10003085842",  # THE HOLLIES, NATTS LANE, BILLINGSHURST
                "100061799860",  # LITTLE BOXES, NATTS LANE, BILLINGSHURST
                "100061816223",  # OLD LAUNDRY COTTAGE, MILL LANE, LOWER BEEDING, HORSHAM
                "10093098746",  # BRIDGE COTTAGE, MILL LANE, LOWER BEEDING, HORSHAM
                "200004790819",  # SADDLERS BUNGALOW, SPEAR HILL, ASHINGTON, PULBOROUGH
                "10013789028",  # LAVENDER COTTAGE, SPEAR HILL, ASHINGTON, PULBOROUGH
                "200004795293",  # WILLIAM PENN FLAT, BLUE IDOL, OLDHOUSE LANE, COOLHAM, HORSHAM
                "10003085561",  # BLUE IDOL RESIDENCE, OLDHOUSE LANE, COOLHAM, HORSHAM
                "100061814530",  # TWO ACRES, LANGHURSTWOOD ROAD, HORSHAM
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "RH12 1HR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Billingshurst Centre, Roman Way, Billingshurst, RH14 9QW
        if record.polling_place_id == "5501":
            record = record._replace(
                polling_place_easting="508896",
                polling_place_northing="126249",
            )

        # more accurate point for: Ravenscroft Guide & Community Centre, Browns Lane, Storrington, RH20 4LQ
        if record.polling_place_id == "5638":
            record = record._replace(
                polling_place_easting="508805",
                polling_place_northing="114119",
            )

        # more accurate point for: Thakeham Village Hall, 1 Abingworth Crescent, Thakeham, RH20 3GW
        if record.polling_place_id == "5646":
            record = record._replace(
                polling_place_easting="510436",
                polling_place_northing="116834",
            )

        return super().station_record_to_dict(record)
