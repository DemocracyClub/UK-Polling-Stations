from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MIK"
    addresses_name = "2021-04-12T09:06:38.958847/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-12T09:06:38.958847/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "8851",  # Stony Stratford Library 5-7 Church Street Stony Stratford Milton Keynes MK11 1BD
            "8915",  # Moorlands Family Centre Dodkin Beanhill MK6 4LP
            "8628",  # St Mary`s Church Newport Road Woughton on the Green Milton Keynes MK6 3BE
        ]:
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "25098995",  # BUNGALOW WOBURN GOLF AND COUNTRY CLUB BOW BRICKHILL TO LITTLE BRICKHILL ROAD, LITTLE BRICKHILL
            "25074114",  # DROPSHORT FARM, WATLING STREET, LITTLE BRICKHILL, MILTON KEYNES
            "25063716",  # SKEW BRIDGE COTTAGE, DRAYTON ROAD, BLETCHLEY, MILTON KEYNES
            "25003647",  # SHENLEY GROUNDS FARM WHADDON ROAD, CALVERTON
            "25107493",  # MAYA LOFT AYLESBURY STREET, WOLVERTON
            "25107492",  # FLAT 1, INCA HOUSE, AYLESBURY STREET, WOLVERTON, MILTON KEYNES
            "25093780",  # NEW FARM HOUSE, PINDON END, HANSLOPE, MILTON KEYNES
            "25093789",  # CARAVAN 2 BLACK HORSE LODGE WOLVERTON ROAD, GREAT LINFORD, MILTON KEYNES
            "25093788",  # CARAVAN 1 BLACK HORSE LODGE WOLVERTON ROAD, GREAT LINFORD, MILTON KEYNES
            "10094484063",  # THE BUNGALOW WOODLEYS FARM BOW BRICKHILL ROAD, WOBURN SANDS
            "10094484064",  # THE COTTAGE WOODLEYS FARM BOW BRICKHILL ROAD, WOBURN SANDS
            "10094480672",  # 5 IVY CLOSE, NEWPORT PAGNELL
        ]:
            return None

        if record.addressline6 in [
            "MK2 2NY",
            "MK13 9DZ",
            "MK13 7NH",
            "MK17 9NH",
            "MK4 4EL",
            "MK4 4AG",
            "MK4 4AU",
            "MK46 5AF",
            "MK46 4JS",
            "MK16 0HW",
            "MK14 6DL",
            "MK12 5LS",
            "MK9 2HS",
            "MK46 5LN",
        ]:
            return None

        return super().address_record_to_dict(record)
