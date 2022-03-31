from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MIK"
    addresses_name = (
        "2022-05-05/2022-03-31T17:15:28.543864/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-31T17:15:28.543864/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Stony Stratford Library 5-7 Church Street Stony Stratford Milton Keynes MK11 1BD
        if record.polling_place_id == "9878":
            # not actually in the sea
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
                polling_place_uprn="25001127",
            )

        # Moorlands Family Centre Dodkin Beanhill MK6 4LP
        if record.polling_place_id == "9938":
            # also not in the sea
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
                polling_place_uprn="10090355529",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "25063716",  # SKEW BRIDGE COTTAGE, DRAYTON ROAD, BLETCHLEY, MILTON KEYNES
            "25107493",  # MAYA LOFT AYLESBURY STREET, WOLVERTON
            "25091328",  # BROUGHTON MANOR, BROUGHTON, MILTON KEYNES
        ]:
            return None

        if record.addressline6 in [
            "MK4 4EL",
            "MK17 8XS",
            "MK13 9DZ",
            "MK4 4AU",
            "MK46 4JS",
            "MK14 6DL",
            "MK4 4AG",
            "MK46 5AF",
            "MK13 7NH",
            "MK7 7FP",
        ]:
            return None

        return super().address_record_to_dict(record)
