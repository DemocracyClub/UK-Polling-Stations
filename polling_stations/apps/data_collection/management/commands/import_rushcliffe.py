from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000176"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Rush.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Rush.csv"
    elections = ["local.2019-05-02"]

    def station_record_to_dict(self, record):

        # these co-ordinates were a missing a digit
        if record.polling_place_id == "4076":
            record = record._replace(polling_place_easting="470360")
        if record.polling_place_id == "4142":
            record = record._replace(polling_place_easting="459770")
        if record.polling_place_id == "4210":
            record = record._replace(polling_place_easting="458380")

        # this one is a last-minute change of venue, not fixing an error
        if record.polling_place_id == "4107":
            record = record._replace(polling_place_name="Cotgrave Scout Hall")
            record = record._replace(polling_place_address_1="Chapel Lane")
            record = record._replace(polling_place_address_2="Cotgrave")
            record = record._replace(polling_place_address_3="Nottingham")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="NG12 3JU")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "3040065651":
            rec["postcode"] = "NG12 4DF"

        if uprn in [
            "3040049104",  # NG122LU -> NG25AS : 4 Adbolton Cottages, Adbolton Lane, Adbolton, Nottingham
            "3040002863",  # LE125RN -> LE125RL : Fox Hill Farm, Stocking Lane, East Leake, Loughborough, Leicestershire
            "3040073217",  # LE125RN -> LE125RL : Bungalow At Foxhill Farm, Stocking Lane, East Leake, Loughborough, Leicestershire
            "3040069354",  # NG116DS -> NG116JY : The Flat, Park House, Mere Way, Ruddington, Nottingham
            "3040001181",  # LE125EH -> LE125EJ : Cold Harbour Farm, Rempstone Road, Normanton on Soar, Loughborough, Leics.
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "3040048625",  # NG122JJ -> NG122LZ : 2 The Lodge, Cropwell Court, Radcliffe Road, Cropwell Butler, Nottingham
            "3040060745",  # NG122JJ -> NG122LZ : Rose Cottage, Cropwell Court, Radcliffe Road, Cropwell Butler, Nottingham
            "3040047261",  # NG124AS -> NG123NU : Golf Course Flat, Wellin Lane, Edwalton, Nottingham
            "3040005836",  # LE126RQ -> LE126XB : Beech Tree Lodge, Costock Road, Rempstone, Loughborough, Leics.
            "3040055327",  # LE126RQ -> LE126XB : Canaan Farm, Loughborough Road, Rempstone, Loughborough, Leics.
            "3040085941",  # NG27YX -> NG27RQ : 1 Woodpecker Close, West Bridgford, Nottingham
            "3040085943",  # NG27YX -> NG27RQ : 5 Woodpecker Close, West Bridgford, Nottingham
            "3040085960",  # NG27YX -> NG27RQ : 4 Woodpecker Close, West Bridgford, Nottingham
            "3040086087",  # NG27UZ -> NG27RN : 13 Starling Close, West Bridgford, Nottingham
            "3040086089",  # NG27UZ -> NG27RN : 11 Starling Close, West Bridgford, Nottingham
            "3040086090",  # NG27UZ -> NG27RN : 10 Starling Close, West Bridgford, Nottingham
            "3040086091",  # NG27UZ -> NG27RN : 9 Starling Close, West Bridgford, Nottingham
            "3040001325",  # NG110AB -> NG110AE : The Old Forge, New Road, Barton In Fabis, Nottingham
            "3040029381",  # NG125BA -> NG125QE : Guys Wood, Widmerpool Lane, Stanton on The Wolds, Nottingham
            "3040073168",  # NG125PS -> NG125QD : Oak Farm House, Fosse Way, Stanton on The Wolds, Nottingham
            "3040051072",  # NG125QQ -> NG125AR : Grange Leys Farm, Keyworth Road, Wysall, Nottingham
            "3040012196",  # NG27AY -> NG123TW : 11 Willow Road, West Bridgford, Nottingham
        ]:
            rec["accept_suggestion"] = False

        return rec
