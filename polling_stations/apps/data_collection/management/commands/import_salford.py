from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000006"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 SalfordCC.tsv"
    )
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 SalfordCC.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012471369",  # M380EL -> M280EL : Peel Mill Cottage, Peel Lane, Little Hulton, Worsley
            "100011389722",  # M272BU -> M276BU : Heath Cottage, 119 Station Road, Pendlebury
            "200001505152",  # M65RA -> M65YD : The Vicarage, 43 Derby Road, Seedley, Salford
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012469873",  # M307RR -> M307QH : Moss Lane Farm, Barton Moss Road, Eccles
            "100011405102",  # M65LS -> M67JT : 39 Duchy Street, Salford
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4087":
            record = record._replace(polling_place_name="The Angel Centre")
            record = record._replace(polling_place_address_1="1 St Philips Place")
            record = record._replace(polling_place_address_2="")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="Salford")
            record = record._replace(polling_place_postcode="M3 6FA")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        rec = super().station_record_to_dict(record)

        if record.polling_place_id == "3897":
            rec["location"] = Point(-2.41516389, 53.51105357, srid=4326)

        return rec
