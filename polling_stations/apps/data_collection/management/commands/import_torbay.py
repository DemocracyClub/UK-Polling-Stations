from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000027"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7553":
            record = record._replace(polling_place_postcode="TQ5 0BX")

        if record.polling_place_id == "7530":
            record = record._replace(polling_place_postcode="TQ5 9HW")

        rec = super().station_record_to_dict(record)

        if record.polling_place_id == "7418":
            rec["location"] = Point(-3.556830, 50.488924, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # This was a last minute import,
        # so I've taken a fairly coarse approach to throwing things away...
        if record.addressline6 in [
            "TQ2 6XA",
            "TQ4 6JX",
            "TQ5 0BX",
            "TQ4 6LH",
            "TQ5 0AE",
            "TQ1 3QF",
            "TQ4",
        ]:
            return None

        if uprn in [
            "100040519265",
            "200002083269",
            "10024003870",
            "10002991569",
            "100040529632",
            "100040562013",
            "100040520900",
            "10093141050",
            "10093141805",
            "10093142379",
            "100040537640",
            "100041189794",
            "10002991567",
            "10002991571",
        ]:
            return None

        if uprn in [
            "100041196260",  # TQ26AS -> TQ26AP : Millbrook House Hotel, Old Mill Road, Torquay
            "200001778568",  # TQ14AF -> TQ14AG : 1C Magdalene Rd Rear Of, 17 Upton Road, Torquay
            "100040561357",  # TQ14LR -> TQ14LH : Flat 2 Westhill Court, 12 Westhill Avenue, Torquay
            "100040561358",  # TQ14LR -> TQ14LH : Flat 3 Westhill Court, 12 Westhill Avenue, Torquay
            "100040559288",  # TQ11EJ -> TQ11EG : 2 Apsley House, Torwood Gardens Road, Torquay
            "100040559289",  # TQ11EJ -> TQ11EG : 3 Apsley House, Torwood Gardens Road, Torquay
            "10002989359",  # TQ50BX -> TQ50BP : The Hayloft, 26 Milton Street, Brixham
        ]:

            rec["accept_suggestion"] = True

        if uprn in [
            "100040523809",  # TQ26AU -> TQ46AU : Cottage C, 1 Old Mill Road, Torquay
            "100041187152",  # TQ12EA -> TQ11BN : Cottage 1 Sundial Lodge, Park Hill Road, Torquay
            "100041187013",  # TQ12EA -> TQ11BN : Mews 8 Sundial Lodge, Park Hill Road, Torquay
            "100040534293",  # TQ32HW -> TQ32SF : Bottom Flat, 239 Torquay Road, Paignton
            "10000012748",  # TQ32HT -> TQ50EH : 1 Manor Court, Manor Road, Paignton
            "10000012807",  # TQ32HT -> TQ50EH : 7 Manor Court, Manor Road, Paignton
            "10000012810",  # TQ32HT -> TQ50EH : 4 Manor Court, Manor Road, Paignton
            "100041195363",  # TQ32HT -> TQ25BZ : 9 Manor Court, Manor Road, Paignton
            "10000012832",  # TQ32HT -> TQ50EH : 5 Manor Court, Manor Road, Paignton
            "10000012760",  # TQ32HT -> TQ50EH : 2 Manor Court, Manor Road, Paignton
            "10000012746",  # TQ32HT -> TQ50EH : 3 Manor Court, Manor Road, Paignton
            "10000012765",  # TQ32HT -> TQ50EH : 6 Manor Court, Manor Road, Paignton
        ]:
            rec["accept_suggestion"] = False

        return rec
