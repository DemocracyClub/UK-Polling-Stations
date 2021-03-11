from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "BUN"
    addresses_name = "2021-03-10T16:07:02.616665/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-10T16:07:02.616665/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Rosewood Primary School Moorland Road Entrance Burnley
        if record.polling_place_id == "4816":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # St Matthews Church Hall Albion Street Burnley
        if record.polling_place_id == "4804":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley
        if record.polling_place_id == "4839":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # Burnley Football Club 1882 Lounge Harry Potts Way Burnley
        if record.polling_place_id == "4776":
            record = record._replace(polling_place_postcode="BB10 4BX")

        # St Cuthbert`s Community Hall Sharp Street Burnley BB10 1UG
        if record.polling_place_id == "4737":
            record = record._replace(polling_place_postcode="BB10 1UJ")

        # Middlesex Over 50s Social Centre, Middlesex Avenue, Burnley
        if record.polling_place_id == "4867":
            record = record._replace(polling_place_postcode="BB12 6AA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023759126",  # ROWLEY HALL FARM, ROWLEY LANE, BURNLEY
            "10023759125",  # THE STABLES, ROWLEY FARM, ROWLEY LANE, BURNLEY
            "10023759124",  # THE COACH HOUSE, ROWLEY FARM, ROWLEY LANE, BURNLEY
            "10023759122",  # ROWLEY COTTAGE, ROWLEY LANE, BURNLEY
            "10023759123",  # ROWLEY HALL, ROWLEY LANE, BURNLEY
            "10023763578",  # FLAT A 66 BRIERCLIFFE ROAD, BURNLEY
        ]:
            return None

        if record.addressline6 in [
            "BB10 3BD",
            "BB10 3PF",
            "BB11 2QR",
            "BB12 8EH",
            "BB10 3JY",
        ]:
            return None

        return super().address_record_to_dict(record)
