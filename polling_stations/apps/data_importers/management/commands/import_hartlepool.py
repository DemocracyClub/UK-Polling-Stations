from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = (
        "2024-07-04/2024-05-28T14:37:51.551024/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T14:37:51.551024/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
            "100110673226",  # TUNSTALL GARTH, ELWICK ROAD, HARTLEPOOL
            "100110673227",  # TUNSTALL HALL FARM, ELWICK ROAD, HARTLEPOOL
            "100110013554",  # 2 GROSMONT ROAD, HARTLEPOOL
            "100110013556",  # 4 GROSMONT ROAD, HARTLEPOOL
            "100110035228",  # 80 WILTSHIRE WAY, HARTLEPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TS25 4PE",
            "TS25 5BF",
            "TS24 9BD",
            "TS24 0PZ",
            "TS25 5QB",
            "TS26 0LA",
            "TS24 8DD",
            "TS24 8PR",
            "TS24 9SF",
            "TS25 5DY",
            # suspect
            "TS25 1EN",
            "TS26 0JD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Gillen Arms Public House, Clavering Road, Hartlepool, TS27 3QY
        if record.polling_place_id == "12762":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.249549, 54.712337, srid=4326)
            return rec

        if record.polling_place_id == "12672":
            # missing postcode and coords correction for:
            # Bowls Pavilion, Ward Jackson Park, The Parade, Hartlepool
            record = record._replace(
                polling_place_postcode="TS26 0BQ",
                polling_place_easting="449116",
                polling_place_northing="532568",
            )

        if record.polling_place_id == "12862":
            # missing postcode for: Divers Club, Harbour Walk, Hartlepool
            record = record._replace(
                polling_place_postcode="TS24 0UX",
            )

        if record.polling_place_id == "12809":
            # missing postcode for: St Columba Centre, Dryden Road, Hartlepool
            record = record._replace(
                polling_place_postcode="TS25 4NY",
            )

        return super().station_record_to_dict(record)
