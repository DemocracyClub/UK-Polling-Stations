from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = (
        "2026-05-07/2026-03-09T16:31:17.161293/Democracy_Club__07May2026 (2).CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-09T16:31:17.161293/Democracy_Club__07May2026 (2).CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090069600",  # THE CARAVAN X-PDI UNIT MIDDLETON ROAD, HARTLEPOOL
            "100110673984",  # ANELVILLE, THROSTON GRANGE LANE, HARTLEPOOL
            "10090073016",  # 319 RABY ROAD, HARTLEPOOL
            "10009715735",  # HOLE HOUSE, WYNYARD, BILLINGHAM
            "10090073376",  # 31 RODNEY STREET, HARTLEPOOL
            "100110013554",  # 2 GROSMONT ROAD, HARTLEPOOL
            "100110013556",  # 4 GROSMONT ROAD, HARTLEPOOL
            "100110035228",  # 80 WILTSHIRE WAY, HARTLEPOOL
            "100110786581",  # TUNSTALL HALL FARM COTTAGE ELWICK ROAD, HARTLEPOOL
            "10095351225",  # FLAT 17 MURRAY STREET, HARTLEPOOL
            "100110673014",  # FULTHORPE COTTAGE, DUCHY ROAD, HARTLEPOOL
            "10095352735",  # 13 WHITEBEAM MEADOWS, HARTLEPOOL
            "10009734017",  # KEEPERS COTTAGE, HART, HARTLEPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TS25 5BF",
            "TS24 9SF",
            "TS25 4PE",
            "TS26 0LA",
            "TS24 9BD",
            "TS25 5QB",
            "TS24 8PR",
            # suspect
            "TS25 1EN",
            "TS26 0JD",
            "TS26 8DD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Gillen Arms Public House, Clavering Road, Hartlepool, TS27 3QY
        if record.polling_place_id == "12959":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.249549, 54.712337, srid=4326)
            return rec

        if record.polling_place_id == "13090":
            # missing postcode and coords correction for:
            # Bowls Pavilion, Ward Jackson Park, The Parade, Hartlepool
            record = record._replace(
                polling_place_postcode="TS26 0BQ",
                polling_place_easting="449116",
                polling_place_northing="532568",
            )

        if record.polling_place_id == "13051":
            # missing postcode for: Divers Club, Harbour Walk, Hartlepool
            record = record._replace(
                polling_place_postcode="TS24 0UX",
            )

        if record.polling_place_id == "13079":
            # missing postcode for: St Columba Centre, Dryden Road, Hartlepool
            record = record._replace(
                polling_place_postcode="TS25 4NY",
            )

        return super().station_record_to_dict(record)
