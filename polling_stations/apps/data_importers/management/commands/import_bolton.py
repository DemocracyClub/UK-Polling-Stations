from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = "2021-05-01T18:52:07.783562/Democracy_Club__06May2021.CSV"
    stations_name = "2021-05-01T18:52:07.783562/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4291":
            # Trinity Methodist Hall (postcode geocode puts this quite away from actual location, making error spotting
            # more difficult)
            record = record._replace(
                polling_place_easting=374156, polling_place_northing=405696
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012434533",  # RATCLIFFES FARM HOUSE, WINGATES LANE, WESTHOUGHTON, BOLTON
            "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
            "100012431797",  # 321 DERBY STREET, BOLTON
            "10001244960",  # FLAT 3, 115-117 DERBY STREET, BOLTON
            "100012556511",  # 152 LONGSIGHT, BOLTON
        ]:
            return None

        # FLAT 1 290 ST HELENS ROAD, BOLTON
        if uprn == "10001244221":
            record = record._replace(property_urn="", post_code="BL1 4JU")

        if record.addressline6 in [
            "BL2 4JU",
            "BL2 3EL",
            "BL2 3BQ",
            "BL2 6DZ",
            "BL1 3QW",
            "BL2 2JU",
            "BL4 8JA",
            "BL1 5DB",
            "BL1 3AU",
            "BL1 5HP",
            "BL1 3SJ",
            "BL1 2HZ",
            "BL3 2DP",
            "BL4 0LW",
            "BL4 7PQ",
            "BL5 2DL",
            "BL4 7BB",
            "BL3 1BA",
            "BL6 4ED",
            "BL6 6PX",
            "BL6 6HN",
            "BL3 6ST",
            "BL4 0HU",
            "BL5 3LT",
            "BL5 2JX",
            "BL5 2DJ",
        ]:
            return None

        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "BL7 OHR":
            rec["postcode"] = "BL7 0HR"

        if record.addressline6.strip() == "BL4 ONX":
            rec["postcode"] = "BL4 0NX"

        if record.addressline6.strip() == "BL4 ONY":
            rec["postcode"] = "BL4 0NY"

        return rec
