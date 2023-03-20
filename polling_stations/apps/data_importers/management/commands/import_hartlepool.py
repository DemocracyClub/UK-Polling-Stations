from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = (
        "2023-05-04/2023-03-20T10:49:01.444458/TEST Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-20T10:49:01.444458/TEST Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100110020667",  # 76 MIDDLETON ROAD, HARTLEPOOL
            "10090069600",  # THE CARAVAN X-PDI UNIT MIDDLETON ROAD, HARTLEPOOL
            "10090070990",  # 2 PHILLIPS ROAD, HARTLEPOOL
            "100110786581",  # TUNSTALL HALL FARM, ELWICK ROAD, HARTLEPOOL
            "100110673984",  # ANELVILLE, THROSTON GRANGE LANE, HARTLEPOOL
            "10090073016",  # 319 RABY ROAD, HARTLEPOOL
            "10009715735",  # HOLE HOUSE, WYNYARD, BILLINGHAM
            "10095352391",  # 17 ASPEN GARDENS, HARTLEPOOL
            "10095352946",  # 42 REEDMACE GARDENS, HARTLEPOOL
            "10095353490",  # 107C PARK ROAD, HARTLEPOOL
            "10090073137",  # 109 GRAYTHORP INDUSTRIAL ESTATE ROAD, HARTLEPOOL
            "100110673014",  # FULTHORPE COTTAGE, DUCHY ROAD, HARTLEPOOL
            "100110035228",  # 80 WILTSHIRE WAY, HARTLEPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TS25 4PE",
            "TS25 5BF",
            "TS24 9BD",
            "TS26 0LA",
            "TS24 0PZ",
            "TS24 8DD",
            "TS25 5QB",
            "TS25 5DY",
            "TS24 8PR",
            "TS24 9SF",
            "TS25 1EN",  # CASTLETON ROAD, HARTLEPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Gillen Arms Public House, Clavering Road, Hartlepool, TS27 3QY
        if rec["internal_council_id"] == "11874":
            rec["location"] = Point(-1.249549, 54.712337, srid=4326)

        return rec
