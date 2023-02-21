from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOS"
    addresses_name = "2021-03-25T12:39:18.697471/Bolsover Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T12:39:18.697471/Bolsover Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Bolsover Parish Rooms, Hornscroft Road, Bolsover, Chesterfield
        if record.polling_place_id == "4511":
            record = record._replace(polling_place_postcode="S44 6HG")

        # The Shoulder at Hardstoft, Hardstoft, Chesterfield, Derbyshire
        if record.polling_place_id == "4490":
            record = record._replace(polling_place_postcode="S45 8AX")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013062215",  # 3 ROTHERHAM ROAD, SCARCLIFFE, CHESTERFIELD
            "10013062214",  # 1 ROTHERHAM ROAD, SCARCLIFFE, CHESTERFIELD
            "10013068383",  # LIVING ACCOMMODATION HORSE AND GROOM MANSFIELD ROAD, SCARCLIFFE
            "10013072767",  # THE FLAT THE CASTLEWOOD PUBLIC HOUSE CARTER LANE EAST, SOUTH NORMANTON
            "200004519933",  # APEX INSULATION SUPPLIES LTD, SAWPIT LANE, TIBSHELF, ALFRETON
        ]:
            return None

        if record.addressline6 in ["NG20 8FJ", "S44 6QH"]:
            return None

        return super().address_record_to_dict(record)
