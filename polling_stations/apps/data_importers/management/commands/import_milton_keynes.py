from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MIK"
    addresses_name = (
        "2023-05-04/2023-03-29T14:16:27.878954/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-29T14:16:27.878954/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "25107493",  # MAYA LOFT AYLESBURY STREET, WOLVERTON
            "25091328",  # BROUGHTON MANOR, BROUGHTON, MILTON KEYNES
            "25092373",  # COOKSOE FARM, CHICHELEY, NEWPORT PAGNELL
            "25093788",  # CARAVAN 1 BLACK HORSE LODGE WOLVERTON ROAD, GREAT LINFORD, MILTON KEYNES
            "10023651529",  # FLAT AT THE BLACK HORSE WOLVERTON ROAD, GREAT LINFORD, MILTON KEYNES
            "25096256",  # 26B STRATFORD ROAD, WOLVERTON, MILTON KEYNES
            "25041362",  # CAFE BUNGALOW, WATLING STREET, ELFIELD PARK, MILTON KEYNES
            "25088205",  # 5 STATION ROAD, WOBURN SANDS, MILTON KEYNES
            "10093919626",  # FLAT 126, SOLSTICE APARTMENTS, 801 SILBURY BOULEVARD, MILTON KEYNES
            "10093919687",  # FLAT 403, SOLSTICE APARTMENTS, 801 SILBURY BOULEVARD, MILTON KEYNES
            "10093919604",  # FLAT 104, SOLSTICE APARTMENTS, 801 SILBURY BOULEVARD, MILTON KEYNES
            "10093919616",  # FLAT 116, SOLSTICE APARTMENTS, 801 SILBURY BOULEVARD, MILTON KEYNES
        ]:
            return None

        if record.addressline6 in [
            "MK13 7NH",
            "MK14 6DL",
            "MK4 4EL",
            "MK46 5AF",
            "MK46 4JS",
            "MK4 4AG",
            "MK4 4AU",
            "MK13 9DZ",
            "MK15 0DW",  # CAMPBELL WHARF MARINA, FROBISHER GATE, NEWLANDS, MILTON KEYNES
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Stony Stratford Library, 5-7 Church Street, Stony Stratford, Milton Keynes, MK11 1BD
        if record.polling_place_id == "10279":
            record = record._replace(
                polling_place_easting="478676",
                polling_place_northing="240427",
            )

        # Moorlands Family Centre, Dodkin Beanhill, MK6 4LP
        if record.polling_place_id == "10605":
            record = record._replace(
                polling_place_easting="486874",
                polling_place_northing="236273",
            )

        # St Mary`s Church, Newport Road, Woughton on the Green, Milton Keynes, MK6 3BE
        if record.polling_place_id == "10465":
            record = record._replace(
                polling_place_easting="487690",
                polling_place_northing="237598",
            )

        return super().station_record_to_dict(record)
