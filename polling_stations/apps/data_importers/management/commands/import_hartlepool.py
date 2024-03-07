from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = "2024-05-02/2024-03-07T09:40:56.937784/Democracy_Club__02May2024 - Polling Stations.tsv"
    stations_name = "2024-05-02/2024-03-07T09:40:56.937784/Democracy_Club__02May2024 - Polling Stations.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100110020667",  # 76 MIDDLETON ROAD, HARTLEPOOL
            "10090069600",  # THE CARAVAN X-PDI UNIT MIDDLETON ROAD, HARTLEPOOL
            "100110786581",  # TUNSTALL HALL FARM, ELWICK ROAD, HARTLEPOOL
            "100110673984",  # ANELVILLE, THROSTON GRANGE LANE, HARTLEPOOL
            "10090073016",  # 319 RABY ROAD, HARTLEPOOL
            "10009715735",  # HOLE HOUSE, WYNYARD, BILLINGHAM
            "10095353814",  # 317 BRENDA ROAD, HARTLEPOOL
            "10090073376",  # 31 RODNEY STREET, HARTLEPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TS24 8PR",
            "TS24 9BD",
            "TS25 5QB",
            "TS25 5BF",
            "TS24 8DD",
            "TS25 5DY",
            "TS24 9SF",
            "TS24 0PZ",
            "TS25 4PE",
            "TS26 0LA",
            # suspect
            "TS25 1EN",  # CASTLETON ROAD, HARTLEPOOL
            "TS26 0JD",  # JESMOND ROAD, HARTLEPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Space To Learn, King Oswy Drive, Hartlepool TS26 0UP
        if record.polling_place_id == "12460":
            record._replace(polling_place_postcode="TS24 9PB")
            return None

        # Gillen Arms Public House, Clavering Road, Hartlepool, TS27 3QY
        if record.polling_place_id == "12354":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.249549, 54.712337, srid=4326)
            return rec

        return super().station_record_to_dict(record)
