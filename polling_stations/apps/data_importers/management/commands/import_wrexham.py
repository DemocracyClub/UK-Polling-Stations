from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRX"
    addresses_name = "2024-05-02/2024-02-22T15:49:07.126386/Wrexham Xpress export Democracy_Club__02May2024 (1).tsv"
    stations_name = "2024-05-02/2024-02-22T15:49:07.126386/Wrexham Xpress export Democracy_Club__02May2024 (1).tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070388463",  # TY HEULOG, CROESHOWELL, LLAY, WREXHAM
            "10004522399",  # GRESFORD HALL, GRESFORD, WREXHAM
            "200002944484",  # ALYN VALE COTTAGE, MOLD ROAD, CEFN-Y-BEDD, WREXHAM
            "100100940769",  # THE WOODLANDS, MOLD ROAD, CEFN-Y-BEDD, WREXHAM
            "200002944484",  # ALYN VALE COTTAGE, MOLD ROAD, CEFN-Y-BEDD, WREXHAM
            "10013546126",  # OLD GATE HOUSE, PENTRE SAESON, BWLCHGWYN, WREXHAM
            "10070390231",  # THE BARN, PENTRE SAESON, BWLCHGWYN, WREXHAM
            "10013545203",  # BARN HILL COTTAGE, RUTHIN ROAD, COEDPOETH, WREXHAM
            "200001858782",  # CROESNEWYDD COTTAGE, CROESNEWYDD ROAD, WREXHAM
            "200001858782",  # CROESNEWYDD COTTAGE, CROESNEWYDD ROAD, WREXHAM
            "10023163146",  # 3 CROESNEWYDD ROAD, WREXHAM
            "10013540479",  # THE CARAVAN BERRYLANDS HOMESTEAD LANE, WREXHAM
            "10070390231",  # THE BARN, PENTRE SAESON, BWLCHGWYN, WREXHAM
            "10004513276",  # Y BWTHYN, LLWYNEINION, RHOSLLANERCHRUGOG, WREXHAM
            "10004512556",  # BRIDGE COTTAGE, TAINANT, PEN-Y-CAE, WREXHAM
            "100100884301",  # BRYN ESTYN, GUTTER HILL, JOHNSTOWN, WREXHAM
            "100100864051",  # POST OFFICE HOUSE, HIGH STREET, RHOSYMEDRE, WREXHAM
            "100100888165",  # ST, WINIFREDS, CHAPEL LANE, CHIRK, WREXHAM
            "10023163579",  # NEW HOUSE FARM, EGLWYS CROSS, WHITCHURCH
            "10013542063",  # THE ELMS, LITTLE GREEN, BRONINGTON, WHITCHURCH
            "10013549854",  # LITTLE GREEN FARM, LITTLE GREEN, BRONINGTON, WHITCHURCH
            "1000452133",  # WITHY GROVE, ELLESMERE ROAD, BRONINGTON, WHITCHURCH
            "10004511906",  # WYEN WERN FARM, SANDY LANE, HANMER, WHITCHURCH
            "200002944623",  # BRYN HOVAH, BANGOR ROAD, OVERTON, WREXHAM
            "200001649414",  # BRYN HOVAH HOUSE, OVERTON ROAD, BANGOR-ON-DEE, WREXHAM
            "200002944623",  # BRYN HOVAH, BANGOR ROAD, OVERTON, WREXHAM
            "10013540361",  # FIVE FORDS COTTAGE, BEDWELL ROAD, CROSS LANES, WREXHAM
            "10023169472",  # SPORTSVIEW, BRYN ESTYN ROAD, WREXHAM
            "200001653877",  # BRAMCOTT, CROESNEWYDD ROAD, WREXHAM
            "100100858230",  # TY DEWR, BRYN ESTYN ROAD, WREXHAM
            "10013540976",  # TINKERS BROOK COTTAGE, ERBISTOCK, WREXHAM
            "100100856052",  # STONE HOUSE, QUARRY ROAD, BRYNTEG, WREXHAM
            "10004522764",  # THE BUNGALOW, CROSS LANE, PENTRE BROUGHTON, WREXHAM
            "200002943992",  # VENARD, CROSS LANE, PENTRE BROUGHTON, WREXHAM
            "100100855073",  # 3A CROSS LANE, PENTRE BROUGHTON, WREXHAM
            "10004523439",  # MAES HEULOG, CHAPEL STREET, PONCIAU, WREXHAM
            "10004526374",  # MERLYS, RUABON ROAD, RUABON, WREXHAM
            "1000452133",  # WITHY GROVE, ELLESMERE ROAD, BRONINGTON, WHITCHURCH
            "100100871128",  # MANAGERS ACCOMMODATION WHEATSHEAF INN MOLD ROAD, GWERSYLLT, WREXHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LL20 7HJ",
            "LL13 9EN",
            "LL13 0YU",
            "LL13 0JW",
            "LL12 8DH",
            "LL13 8US",
            "SY13 3BU",
            "LL11 4UY",
            "LL12 0RY",
            # looks wrong
            "LL12 0HE",
            "LL11 3EZ",
            "LL14 5BG",
            "LL12 0DF",
            "LL139US",
            "LL11 6AF",
            "LL11 4TT",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Friends Meeting House, Holt Road, Wrexham
        if record.polling_place_id == "9110":
            record = record._replace(polling_place_postcode="LL13 8HN")

        # postcode correction for: Gresford Methodist Church Hall, Chester Road, Gresford, Wrexham
        if record.polling_place_id == "8954":
            record = record._replace(polling_place_postcode="LL12 8PA")

        # postcode correction for: Gwersyllt Congregational Church, 3 Dodds Lane, Gwersyllt, Wrexham, LL11 4LG
        # requested by the council
        if record.polling_place_id == "8992":
            record = record._replace(polling_place_postcode="LL11 4NT")

        # council request to replace old station: St Mary`s School Community Room, Park Street, Ruabon, Wrexham, LL14 6LE
        # with new: St Mary’s Church Hall, 3 Church Street, Ruabon, Wrexham, LL14 6DS
        if record.polling_place_id == "9100":
            record = record._replace(polling_place_name="St Mary’s Church Hall")
            record = record._replace(polling_place_address_1="3 Church Street")
            record = record._replace(polling_place_address_2="Ruabon")
            record = record._replace(polling_place_address_3="Wrexham")
            record = record._replace(polling_place_postcode="LL14 6DS")

        return super().station_record_to_dict(record)
