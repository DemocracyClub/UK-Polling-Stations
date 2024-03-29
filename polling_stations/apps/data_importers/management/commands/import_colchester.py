from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2024-05-02/2024-03-01T11:57:47.053594/Democracy_Club__02May2024 (7).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-01T11:57:47.053594/Democracy_Club__02May2024 (7).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Old Heath Community Centre, D'Arcy Road, Old Heath, Colchester, CO2 8BB
        if record.polling_place_id == "12587":
            record = record._replace(polling_place_postcode="CO2 8BA")
        # Pegasus Club, Circular Road North, Colchester
        if record.polling_place_id == "12869":
            record = record._replace(
                polling_place_easting="599469", polling_place_northing="224341"
            )
        # St. Margaret`s Church Hall, Stansted Road, Colchester
        if record.polling_place_id == "12538":
            record = record._replace(
                polling_place_easting="600304", polling_place_northing="222358"
            )
        # Quaker Meeting House, 6 Church Street, Colchester
        if record.polling_place_id == "12545":
            record = record._replace(
                polling_place_easting="599320", polling_place_northing="225080"
            )
        # Tiptree United Reformed Church Hall, Chapel Road, Tiptree
        if record.polling_place_id == "12753":
            record = record._replace(
                polling_place_easting="590290", polling_place_northing="216096"
            )
        # Little Horkesley Village Hall, School Lane, School Road, Little Horkesley, Colchester
        if record.polling_place_id == "12786":
            record = record._replace(
                polling_place_easting="595929", polling_place_northing="232104"
            )
        # Aldham Village Hall, Tey Road, Aldham, Colchester
        if record.polling_place_id == "12794":
            record = record._replace(
                polling_place_easting="591699", polling_place_northing="225838"
            )
        # Church of Jesus Christ of Latter Day Saints, 272 Straight Road, Colchester
        if record.polling_place_id == "12655":
            record = record._replace(
                polling_place_easting="596737", polling_place_northing="223633"
            )
        # Colchester Croquet Club, 16 Elianore Road, Lexden, Colchester
        if record.polling_place_id == "12871":
            record = record._replace(
                polling_place_easting="597712", polling_place_northing="225301"
            )
        # Mount Bures Village Hall, Craigs Lane, Mount Bures, Bures
        if record.polling_place_id == "12806":
            record = record._replace(
                polling_place_easting="590570", polling_place_northing="232698"
            )
        # St. John`s & Highwoods Community Centre, Highwoods Square, Colchester
        if record.polling_place_id == "12590":
            record = record._replace(
                polling_place_easting="600863", polling_place_northing="227637"
            )
        # Easthorpe Church Hall, Easthorpe Road, Easthorpe, Colchester
        if record.polling_place_id == "12757":
            record = record._replace(
                polling_place_easting="591266", polling_place_northing="221514"
            )
        # Messing Village Hall, The Street, Messing, Colchester
        if record.polling_place_id == "12731":
            record = record._replace(
                polling_place_easting="589636", polling_place_northing="218945"
            )
        # Chappel & Wakes Colne Village Hall, Colchester Road, Wakes Colne, Colchester
        if record.polling_place_id == "12798":
            record = record._replace(
                polling_place_easting="589422", polling_place_northing="228582"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER
            "10095445911",  # 32D MAYPOLE GREEN ROAD, COLCHESTER
        ]:
            return None
        if record.addressline6 in [
            # split
            "CO2 8BU",
            "CO4 5LG",
            "CO6 1HA",
        ]:
            return None

        return super().address_record_to_dict(record)
