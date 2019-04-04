from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000024"
    addresses_name = "local.2019-05-02/Version 1/n-somerset.gov.uk-1552316467000.tsv"
    stations_name = "local.2019-05-02/Version 1/n-somerset.gov.uk-1552316467000.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "6470":
            record = record._replace(
                polling_place_name="Wick St. Lawrence Village Hall"
            )
            record = record._replace(polling_place_address_1="Wick St. Lawrence")
            record = record._replace(polling_place_address_2="")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="BS22 7YP")
            record = record._replace(polling_place_easting="336512")
            record = record._replace(polling_place_northing="165164")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "24146745":
            rec["postcode"] = "BS20 0QH"

        if uprn == "34133047":
            rec["postcode"] = "BS23 3AN"

        if uprn == "24147349":
            return None

        if uprn in [
            "24092470",  # BS407AP -> BS407AW : Ham Cottage, Rickford Rise, Burrington, Bristol
            "24080870",  # BS483PB -> BS483QA : Backwell House, Farleigh Road, Backwell, Bristol
            "24057302",  # BS207SB -> BS207SD : The Beeches, Cadbury Camp Lane, Clapton-in-Gordano, Bristol
            "24127494",  # BS227RJ -> BS207RJ : Clapton Court, Clevedon Lane, Clapton-in-Gordano, Bristol
            "24124333",  # BS216RJ -> BS216RN : Wyhol Bungalow, Cadbury Camp Lane West, Tickenham, Nr. Clevedon, Somerset
            "24036314",  # BS226EA -> BS227FA : 37 Ellis Park, St Georges, Weston-super-Mare
            "24091741",  # BS216UB -> BS216TZ : Woodruff, Kennmoor Road, Kenn, Clevedon
            "24012365",  # BS232LG -> BS232LQ : Alice House, 6/8 Queens Road, Weston-super-Mare
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "24123333",  # BS231DE -> BS216RD : Flat C, First and Second Floor, 79 Clevedon Road, Weston-super-Mare
            "24123334",  # BS231DE -> BS216RD : Flat B, 79 Clevedon Road, Weston-super-Mare
            "24058849",  # BS405HU -> BS233SD : The Hall, Langford Road, Langford, Bristol
            "24121026",  # BS207TR -> BS249SG : The Old Dairy, Church Lane, Portbury, Bristol
            "24126251",  # BS232UU -> BS232UP : The Coach House, 87A Milton Road, Weston-super-Mare
            "24083631",  # BS249SH -> BS240AD : Keeper`s Cottage, 1 Upper Church Lane, Hutton, Weston-super-Mare
            "24123490",  # BS234DB -> BS206YF : Ground Floor Flat, 12 Exeter Road, Weston-super-Mare
            "24000034",  # BS229YD -> BS232EP : Wayside, 3 Kewstoke Road, Kewstoke, Weston-super-Mare
            "24024127",  # BS229LF -> BS229YH : 88 Lower Kewstoke Road, Weston-super-Mare
            "24122755",  # BS494LH -> BS494LW : Streamcross Community Church, 181 Claverham Road, Claverham, Bristol
            "24042019",  # BS216XD -> BS216NB : Woodview, Kingston Seymour, Clevedon
            "24127398",  # BS138AH -> BS405RB : The Town & Country Lodge, Bridgwater Road, Long Ashton, Bristol
            "24009435",  # BS231NA -> BS231NR : 20 Boulevard, Weston-super-Mare
            "24084780",  # BS206AY -> BS206AZ : Yew Tree House, Forehills Road, Portishead, Bristol
            "24083287",  # BS217AZ -> BS217AX : Woodbine Cottage, Walton Bay, Walton-in-Gordano, Clevedon
            "24083315",  # BS217AS -> BS217AZ : Harvest Home, Walton Bay, Walton-in-Gordano, Clevedon
            "24141641",  # BS233UE -> BS227FP : Flat 1, 8 Chaucer Road, Weston-super-Mare
            "24124873",  # BS246SQ -> BS246SG : Heathgate Paddock, Bristol Road, Hewish, Weston-super-Mare
        ]:
            rec["accept_suggestion"] = False

        return rec
