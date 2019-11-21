from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000026"
    addresses_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # Community Centre, Warwickshire Shopping Park
        if record.polling_place_id == "11876":
            record = record._replace(polling_place_postcode="CV3 2SB")

        # Parkgate Primary School
        if record.polling_place_id == "11954":
            record = record._replace(polling_place_postcode="CV6 4GF")

        if record.polling_place_id == "12190":
            record = record._replace(polling_place_easting="429643")
            record = record._replace(polling_place_northing="278413")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() in [
            "CV3 1QH",
            "CV4 9AJ",
            "CV4 9YJ",
            "CV6 2GE",
            "CV6 2EQ",
        ]:
            return None

        if uprn == "100071317687":
            rec["postcode"] = "CV12LL"

        if uprn in [
            "100071319791",  # CV59AP -> CV59AR : The Cottage, Pickford Grange Lane, Coventry
            "100071367442",  # CV24ED -> CV24EB : 74 Walsgrave Road, Coventry
            "10024031054",  # CV36BQ -> CV36PB : 54 Kenpas Highway, Coventry
            "10024625018",  # CV35FE -> CV12NJ : Annex at 39 Quinton Road, Coventry
            "10024029198",  # CV14AQ -> CV13BW : Flat F, 4 Barras Lane, Coventry
            "100071316737",  # CV62AG -> CV62AL : The Nugget, Hollyfast Road, Coventry
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100071505028",  # CV35AX -> CV35DU : Cornerpost Public House, Watercall Avenue, Coventry
            "10024621865",  # CV64GR -> CV78RH : 26 Gospel Oak Road, Coventry
            "10024621863",  # CV64GS -> CV78RH : 1 Gospel Oak Road, Coventry
            "100070634208",  # CV24LJ -> CV24LS : 17 Clay Lane, Stoke, Coventry
            "100070624242",  # CV32DS -> CV32HZ : 13 Brinklow Road, Coventry
            "100070715099",  # CV57BP -> CV57LJ : Tiber Cottage, Tiber Close, Coventry
            "10024028272",  # CV66BL -> CV62BL : FLAT ABOVE, 267 - 269 Bedworth Road, Coventry
            "200001562367",  # CV63BP -> CV63HL : Caretakers Flat Westfield House, Radford Road, Coventry
            "10024620573",  # CV21UR -> CV61PR : 12 Curlew Close, Coventry
            "10024621864",  # CV64GR -> CV78RH : 58 Gospel Oak Road, Coventry
        ]:
            rec["accept_suggestion"] = False

        if uprn in [
            # Addressbase issues - TODO: report to OS
            "10023038958",
            "100070637150",
            "10024027630",
            "100071317687",
            "10024027756",
            "10023038958",
            "10023034814",
            "10023034813",
            "10023034811",
            "10023034810",
            "10023034809",
            "10023034808",
        ]:
            rec["accept_suggestion"] = False

        return rec
