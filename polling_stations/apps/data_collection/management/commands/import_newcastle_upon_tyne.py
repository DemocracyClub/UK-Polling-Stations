from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000021"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019new.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019new.CSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.polling_place_id == "9069":
            record = record._replace(polling_place_address_1="Blucher Colliery Road")
            record = record._replace(polling_place_address_2="Blucher")
            record = record._replace(polling_place_address_3="Newcastle upon Tyne")
            record = record._replace(polling_place_postcode="NE15 9SD")

        # Station changes for EU election
        if record.polling_place_id == "8809":
            record = record._replace(
                polling_place_name="Stanton Street Community Lounge"
            )
            record = record._replace(polling_place_address_1="Stanton Street")
            record = record._replace(polling_place_address_2="Newcastle upon Tyne")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="NE4 5LH")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        if record.polling_place_id == "9008":
            record = record._replace(polling_place_name="St Charles Church")
            record = record._replace(polling_place_address_1="Church Road")
            record = record._replace(polling_place_address_2="Gosforth")
            record = record._replace(polling_place_address_3="Newcastle upon Tyne")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="NE3 1TX")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "4510740026":
            rec["postcode"] = "NE14HZ"
            rec["accept_suggestion"] = False

        if uprn == "4510732863":
            rec["postcode"] = "NE21XJ"
            rec["accept_suggestion"] = False

        if uprn in [
            "4510745487",  # NE49NQ -> NE45NQ : Flat 7, 4 Callerton Place, Newcastle upon Tyne
            "4510745489",  # NE49NQ -> NE45NQ : Flat 9, 4 Callerton Place, Newcastle upon Tyne
            "4510717900",  # NE77DU -> NE77DT : 26A Benton Road, Newcastle upon Tyne
            "4510714381",  # NE137AP -> NE137AS : Morley Hill Farm, Coach Lane, Newcastle upon Tyne
            "4510113448",  # NE62FW -> NE62BA : 40 St. Peter`s Road, Newcastle upon Tyne
            "4510113447",  # NE62FW -> NE62BA : 38 St. Peter`s Road, Newcastle upon Tyne
            "4510107619",  # NE48XS -> NE48XT : Caretakers House, Atkinson Road School, Atkinson Road, Newcastle upon Tyne
            "4510138256",  # NE12BR -> NE12AF : Penthouse Salvation Army Res Centre, 39 City Road, Newcastle upon Tyne
            "4510138256",  # NE12BR -> NE12AF : Salvation Army Res Centre, 39 City Road, Newcastle upon Tyne
            "4510742753",  # NE21AA -> NE24AA : Flat G 1, 23 Claremont Place, Newcastle upon Tyne
            "4510742754",  # NE21AA -> NE24AA : Flat G 2, 23 Claremont Place, Newcastle upon Tyne
            "4510742755",  # NE21AA -> NE24AA : Flat G 3, 23 Claremont Place, Newcastle upon Tyne
            "4510052253",  # NE52JH -> NE55JH : 111 West Avenue, Newcastle upon Tyne
            "4510052225",  # NE55JH -> NE55LE : Woodhouse, West Avenue, Newcastle upon Tyne
            "4510130828",  # NE22AH -> NE21JS : Ground Floor Flat, 35A Osborne Road, Newcastle upon Tyne
            "4510027740",  # NE32SH -> NE32HJ : 2 Park Avenue, Newcastle upon Tyne
            "4510748969",  # NE65AP -> NE65HP : 188B Heaton Park Road, Newcastle upon Tyne
            "4510741139",  # NE51QF -> NE52QF : 3 Fourstones Mews, Newcastle upon Tyne
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "4510737461",  # NE14SL -> NE157AF : Flat 123 The View, Barrack Road, Newcastle upon Tyne
            "4510118090",  # NE62QN -> NE62NX : School House, Bywell Street, Newcastle upon Tyne
            "4510737021",  # NE139DB -> NE14LB : 75 Greville Gardens, Newcastle upon Tyne
            "4510740467",  # NE12QF -> NE63LY : 18A Orb Building True Student, Coquet Street, Newcastle upon Tyne
            "4510741266",  # NE139AY -> NE65AH : 1, Abberwick Walk, Newcastle upon Tyne
            "4510740467",  # NE12QF -> NE63LY : 18B Orb Building True Student, Coquet Street, Newcastle upon Tyne
        ]:
            rec["accept_suggestion"] = False

        return rec
