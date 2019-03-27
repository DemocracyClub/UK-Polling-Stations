from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000019"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19sheff.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19sheff.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode == "S20 3FS":
            return None

        if record.houseid == "3071121":
            rec["postcode"] = "S17 4AT"
            rec["accept_suggestion"] = False

        if uprn in [
            "10022927869",  # S24NA -> S14RQ : Apartment 7 2 Mary Street, Sheffield
            "100050961874",  # S118TB -> S118TD : Flat Over 782 Ecclesall Road, Sheffield
            "10003572911",  # S80RL -> S80RN : Flat Over 67 Chesterfield Road, Sheffield
            "100051115645",  # S80PL -> S80NT : Apartment 2 67 Smithy Wood Crescent, Sheffield
            "100051115646",  # S80PL -> S80NT : Apartment 1 67 Smithy Wood Crescent, Sheffield
            "100051072577",  # S117AA -> S118ZP : Over 398 Sharrow Vale Road, Sheffield
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100052084411",  # S118RQ -> S118RP : Coach House 11 Brocco Bank, Sheffield
            "10023155059",  # S11HA -> S57EH : Archer Project Sheffield Cathedral Church Street, Sheffield
            "10090614322",  # S80ZH -> S87LD : 88 Chippinghouse Road, Sheffield
            "100051004490",  # S117TG -> S103TE : School House Ivy Cottage Lane, Sheffield
            "100050928743",  # S104PE -> S104QX : Soughley Cottage Brown Hills Lane, Sheffield
            "10003573730",  # S66GH -> S66GD : Fern Hill Hollow Meadows, Sheffield
            "10013159987",  # S66GQ -> S66LJ : 1 Trouble Wood Lane, Sheffield
            "10013159991",  # S66GQ -> S66LJ : 2 Trouble Wood Lane, Sheffield
            "10094032044",  # S66GQ -> S66LJ : 3 Trouble Wood Lane, Sheffield
            "100051072776",  # S124LW -> S124LT : The Fairway 162 Sheffield Road, Hackenthorpe, Sheffield
            "200002991853",  # S137PL -> S124LP : 1 Beighton Road, Sheffield
            "200003018213",  # S101QS -> S101QN : 8 Northfield Road, Sheffield
            "10003576025",  # S64HA -> S64GW : Over 49 Middlewood Road, Sheffield
            "200003024433",  # S62DH -> S64HB : Hillsborough Park Lodge 947 Penistone Road, Sheffield
            "200003000612",  # S25RS -> S25QQ : 192 Long Henry Row, Sheffield
            "200003000616",  # S25RS -> S25QQ : 196 Long Henry Row, Sheffield
            "200002999863",  # S25RH -> S25QQ : 176 Norwich Row, Sheffield
            "200002999864",  # S25RH -> S25QQ : 177 Norwich Row, Sheffield
            "200002999874",  # S25RH -> S25QQ : 187 Norwich Row, Sheffield
            "200002999883",  # S25RH -> S25QQ : 196 Norwich Row, Sheffield
            "200002999897",  # S25RH -> S25QQ : 210 Norwich Row, Sheffield
            "200002999315",  # S25RH -> S25QQ : 222 Norwich Row, Sheffield
            "200002999318",  # S25RH -> S25QQ : 225 Norwich Row, Sheffield
            "200002999858",  # S25RG -> S25QQ : 98 Norwich Row, Sheffield
            "200003016406",  # S66LJ -> S66LH : Ashley Cottage High Bradfield, Sheffield
            "200003021852",  # S363ZB -> S363ZA : Yew Trees Cottage Yew Trees Lane, Bolsterstone, Sheffield
            "200003021853",  # S363ZB -> S363ZA : Yew Trees Farm Yew Trees Lane, Bolsterstone, Sheffield
            "100050981171",  # S361LL -> S364GH : The Cruck Barn Green Farm Green Lane, Stocksbridge, Sheffield
            "200003025132",  # S362PR -> S362NR : The Boskins Royd Farm Carr Road, Deepcar, Sheffield
        ]:
            rec["accept_suggestion"] = False

        return rec
