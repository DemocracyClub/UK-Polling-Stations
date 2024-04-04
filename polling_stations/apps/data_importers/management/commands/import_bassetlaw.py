from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)
from django.contrib.gis.geos import Point


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "BAE"
    addresses_name = (
        "2024-05-02/2024-02-28T19:57:25.344833/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-28T19:57:25.344833/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090589160",  # ROSE BANK, MAIN STREET, NORTH LEVERTON, RETFORD
            "100032031084",  # WILLOW LODGE, LEVERTON ROAD, RETFORD
            "10023264273",  # LOCK KEEPERS COTTAGE, WHARF ROAD, RETFORD
            "100031268741",  # THE OLD LODGE, BABWORTH, RETFORD
            "100031268740",  # SWISS COTTAGE, BABWORTH, RETFORD
            "10013978440",  # STATION HOUSE, FLEDBOROUGH, NEWARK
            "10013976977",  # DOVER LODGE, DOVER BOTTOM, ELKESLEY, RETFORD
            "10013976869",  # WEST LODGE, OSBERTON, WORKSOP
            "10013975796",  # LILAC COTTAGE, OSBERTON, WORKSOP
            "10013973556",  # WEDDING DRIVE LODGE, WELBECK, WORKSOP
            "10013978834",  # COLLINGTHWAITE FARM, CUCKNEY, MANSFIELD
            "100031283284",  # 298 CARLTON ROAD, WORKSOP
            "100031285616",  # HODSOCK GRANGE, DONCASTER ROAD, LANGOLD, WORKSOP
            "10023268927",  # LOW FARM, GROVE, RETFORD
            "10023264575",  # D SKELTON SONS, BISHOPFIELD FARM, SERLBY, DONCASTER
            "10013975962",  # THE CARAVAN DANESHILL PIGGERIES DANESHILL ROAD, LOUND
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DN22 8AH",
            "S80 1QU",
            "S80 2DS",
            # looks wrong
            "DN11 8GF",
            "DN22 7SH",
            "DN22 8BJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction from council for: Manton Parish Hall, 2a Cavendish Road, Worksop S80 2PG
        if record.polling_place_id == "13051":
            record = record._replace(polling_place_postcode="S80 2ST")

        # postcode correction for: Carlton Youth Centre, Lawn Road, Costhorpe, Worksop, S81 9RJ
        if record.polling_place_id == "12787":
            record = record._replace(polling_place_postcode="S81 9LB")

        # added postcode for: Lound Village Hall, Town Street, Lound, Retford, Notts
        if record.polling_place_id == "12941":
            record = record._replace(polling_place_postcode="DN22 8RX")

        # added postcode for: Barnby Moor Village Hall, Kennel Drive, Barnby Moor, Retford, Notts
        if record.polling_place_id == "12939":
            record = record._replace(polling_place_postcode="DN22 8QU")

        # added postcode for: Harworth & Bircotes Town Hall, Scrooby Road, Harworth, Doncaster
        if record.polling_place_id == "12892":
            record = record._replace(polling_place_postcode="DN11 8JP")

        # postcode correction for: Walks of Life Museum, 33 Lincoln Road, Tuxford, NG22 OHR
        if record.polling_place_id == "13126":
            record = record._replace(polling_place_postcode="NG22 0HR")

        rec = super().station_record_to_dict(record)

        # correction brought forward from locals: Manton Parish Hall, 2a Cavendish Road, S80 2PG
        if record.polling_place_id == "13051":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
