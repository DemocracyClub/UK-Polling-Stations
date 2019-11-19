from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000001"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019Bolton.CSV"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Bolton.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "3670":
            # Trinity Methodist Hall (postcode geocode puts this quite away from actual location, making error spotting
            # more difficult)
            record = record._replace(
                polling_place_easting=374156, polling_place_northing=405696
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.property_urn == "10001244221":
            record = record._replace(property_urn="", post_code="BL1 4JU")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "BL7 OHR":
            rec["postcode"] = "BL7 0HR"

        if record.addressline6.strip() == "BL4 ONX":
            rec["postcode"] = "BL4 0NX"

        if record.addressline6.strip() == "BL4 ONY":
            rec["postcode"] = "BL4 0NY"

        if uprn == "100010854762":
            rec["postcode"] = "BL3 4BG"

        if uprn in ["100010864955", "100010864956"]:
            rec["postcode"] = "BL5 3QW"

        if record.addressline6.strip() in ("BL4 9AJ",):
            return None

        if record.addressline1.endswith(" The Hollins Halls of Residence"):
            # Postcode wrong in AddressBase, according to the web
            rec["accept_suggestion"] = False

        if uprn in [
            "100010900195",  # BL24JU -> BL23JL : 32 Longsight Lane, Harwood, Bolton, Lancs
            "100010900196",  # BL24JU -> BL23JR : The Bungalow, 33 Longsight Lane, Harwood, Bolton, Lancs
            "100010900240",  # BL24JU -> BL24BA : 215 Longsight Lane, Harwood, Bolton, Lancs
            "100012432800",  # BL24JU -> BL24LB : Hawthorne Cottage, Longsight Lane, Harwood, Bolton, Lancs
            "100012432803",  # BL24JU -> BL24JX : Longworth Manor, Longsight Lane, Harwood, Bolton, Lancs
            "200002549966",  # BL23BQ -> BL24BQ : 105 Lea Gate, Bradshaw, Bolton, Lancs
            "200002549967",  # BL23BQ -> BL24BQ : 107 Lea Gate, Bradshaw, Bolton, Lancs
            "100010930105",  # BL24JA -> BL24HR : 85 Stitch-Mi-Lane, Harwood, Bolton, Lancs
            "100010930106",  # BL24JA -> BL24HR : 87 Stitch-Mi-Lane, Harwood, Bolton, Lancs
            "100010922768",  # BL52DL -> BL51DL : 101 Rutherford Drive, Over Hulton, Bolton, Lancs
            "100012555302",  # BL66PX -> BL17PX : Bob Smithy, 1450 & 1448 Chorley Old Road, Bolton, Lancs
            "100010897318",  # BL52JX -> BL52JZ : Ground Floor Flat, 300 Leigh Road, Westhoughton, Bolton, Lancs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013876189",  # BL17LA -> BL53DR : 1A Park Terrace, Bolton, Lancs
            "100010922976",  # BL49HG -> BL15LJ : 19 Norris Street, Farnworth, Bolton, Lancs
            "100010922977",  # BL49HG -> BL15LJ : 21 Norris Street, Farnworth, Bolton, Lancs
            "100010922978",  # BL49HG -> BL15LJ : 23 Norris Street, Farnworth, Bolton, Lancs
            "10070921264",  # BL79GX -> BL65LJ : 54 Clarendon Gardens, Bromley Cross, Bolton, Lancs
            "10070920393",  # BL79SZ -> BL25DR : 9 Bedford Street, Egerton, Bolton, Lancs
            "10070923602",  # BL22LA -> BL26BB : 398 Tonge Moor Road, Bolton, Lancs
            "10070919948",  # BL35QU -> BL24LL : First Floor, 333 Wigan Road, Bolton, Lancs
            "100010865555",  # BL15GJ -> BL34HY : 28 Clevelands Drive, Bolton, Lancs
            "100010871529",  # BL14SE -> BL35HH : 249 Spa Road, Bolton, Lancs
            "100010868073",  # BL47QX -> BL32LZ : 27 Darley Street, Farnworth, Bolton, Lancs
            "100010873637",  # BL13QW -> BL18DS : 35 Draycott Street, Bolton, Lancs
            "10070920228",  # BL47AT -> BL49PF : Flat 10 Alan Ball House, 89 Bolton Road, Farnworth, Bolton, Lancs
            "100012558352",  # BL33LB -> BL33JU : First Floor Flat, 187 Morris Green Lane, Bolton, Lancs
            "100012558463",  # BL33LB -> BL33JU : Ground Floor Flat, 187 Morris Green Lane, Bolton, Lancs
            "100012431165",  # BL47SL -> BL47SF : Cemetery Lodge, Cemetery Road, Kearsley, Bolton, Lancs
            "100010863119",  # BL15DP -> BL66JT : Flat Above, 543 Chorley New Road, Bolton, Lancs
            "100010942100",  # BL34QH -> BL52BS : 446 Wigan Road, Bolton, Lancs
            "100010871458",  # BL35HJ -> BL34EU : Flat 1, 352 Deane Road, Bolton, Lancs
            "10001246600",  # BL15PS -> BL15NH : 2 Markland Hill Lane, Bolton, Lancs
            "100010901886",  # BL32LS -> BL23JZ : Hardman Fold Lodge, 3 Lynwood Avenue, Bolton, Lancs
        ]:
            rec["accept_suggestion"] = False

        return rec
