from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)
from django.contrib.gis.geos import Point


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "BAE"
    addresses_name = (
        "2025-05-01/2025-02-26T16:23:06.802866/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-26T16:23:06.802866/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090589160",  # ROSE BANK, MAIN STREET, NORTH LEVERTON, RETFORD
            "100032031084",  # WILLOW LODGE, LEVERTON ROAD, RETFORD
            "10013976977",  # DOVER LODGE, DOVER BOTTOM, ELKESLEY, RETFORD
            "10013976869",  # WEST LODGE, OSBERTON, WORKSOP
            "10013975796",  # LILAC COTTAGE, OSBERTON, WORKSOP
        ]:
            return None

        if record.addressline6 in [
            # splits
            "S81 9GN",
            "DN22 8AH",
            "S80 1QU",
            "S80 2DS",
            "S81 9FD"
            # looks wrong
            "DN11 8GF",
            "DN22 7SH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # added postcode for: Lound Village Hall, Town Street, Lound, Retford, Notts
        if record.polling_place_id == "15364":
            record = record._replace(polling_place_postcode="DN22 8RX")

        # added postcode for: Barnby Moor Village Hall, Kennel Drive, Barnby Moor, Retford, Notts
        if record.polling_place_id == "15231":
            record = record._replace(polling_place_postcode="DN22 8QU")

        # added postcode for: Harworth & Bircotes Town Hall, Scrooby Road, Harworth, Doncaster
        if record.polling_place_id == "15399":
            record = record._replace(polling_place_postcode="DN11 8JP")

        rec = super().station_record_to_dict(record)

        # correction brought forward from locals: Manton Parish Hall, 2a Cavendish Road, S80 2PG
        if record.polling_place_id == "15494":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
