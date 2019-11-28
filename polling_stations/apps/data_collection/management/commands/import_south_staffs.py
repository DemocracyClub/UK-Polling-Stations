from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000196"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019sstaffs.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019sstaffs.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3464":
            record = record._replace(
                polling_place_easting="391056", polling_place_northing="319891"
            )

        if record.polling_place_id == "3427":
            record = record._replace(
                polling_place_easting="389364", polling_place_northing="295314"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004532518",
            "100031812029",
            "10003692636",
        ]:
            return None

        if record.addressline6 in ["DY7 5HL", "ST19 5RH"]:
            return None

        if uprn == "200004533338":
            rec["postcode"] = "DY6 0BD"
        if uprn == "100031830402":
            rec["postcode"] = "WV4 4UF"
        if uprn == "100031816788":
            rec["postcode"] = "WV6 7BP"
        if uprn == "200004534131":
            rec["postcode"] = "WV6 7HB"

        if uprn in [
            "100031809999",  # WS67AD -> WS67AF : 2 Pinfold House, High Street, Cheslyn Hay, South Staffordshire
            "100031810022",  # WS67AD -> WS67AF : 25 Pinfold House, High Street, Cheslyn Hay, South Staffordshire
            "200002877369",  # WS67NY -> WS67HP : 30 Pinfold Lane, Cheslyn Hay, South Staffordshire
            "200002877370",  # WS67NY -> WS67HP : 32 Pinfold Lane, Cheslyn Hay, South Staffordshire
            "200004526137",  # ST195PQ -> ST195PG : Holding, 138 Rodbaston Drive, Rodbaston, Stafford, Staffordshire
            "200004526144",  # ST195PQ -> ST195PG : Stable Farm, Rodbaston Drive, Rodbaston, Stafford, Staffordshire
            "200004526145",  # ST195PQ -> ST195PG : Holding, 139 Rodbaston Drive, Rodbaston, Stafford, Staffordshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100031811670",  # WS67BL -> WS67BH : 17 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811673",  # WS67BL -> WS67BH : 20 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811675",  # WS67BL -> WS67BH : 22 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811676",  # WS67BL -> WS67BH : 23 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811677",  # WS67BL -> WS67BH : 24 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811678",  # WS67BL -> WS67BH : 25 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811680",  # WS67BL -> WS67BH : 27 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811682",  # WS67BL -> WS67BH : 29 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811685",  # WS67BL -> WS67BH : 35 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811686",  # WS67BL -> WS67BH : 37 New Horse Road, Cheslyn Hay, South Staffordshire
            "100031811687",  # WS67BL -> WS67BH : 39 New Horse Road, Cheslyn Hay, South Staffordshire
            "10090090463",  # WV107DW -> WV107DJ : The Meadows Vicarage Road, Vicarage Road, Calf Heath, Wolverhampton, South Staffordshire
            "100031830915",  # WV107DW -> WV107DL : Willow Cottage, Straight Mile, Calf Heath, Wolverhampton
            "100031830921",  # WV107DW -> WV107DL : Ash House, Straight Mile, Calf Heath, Wolverhampton
            "100031830923",  # WV107DW -> WV107DL : High Clere, Straight Mile, Calf Heath, Wolverhampton
            "100031830924",  # WV107DW -> WV107DL : Meadow View, Straight Mile, Calf Heath, Wolverhampton
            "100031830925",  # WV107DW -> WV107DL : Oakland, Straight Mile, Calf Heath, Wolverhampton
            "100032229602",  # WV107DW -> WV107DL : Mile End Cottage, Straight Mile, Calf Heath, Wolverhampton
            "200004532613",  # WV107DW -> WV107DL : Newhaven, Straight Mile, Calf Heath, Wolverhampton
            "200004529818",  # WV107BN -> WV95AW : The Harrows, Stafford Road, Standeford, Wolverhampton
        ]:
            rec["accept_suggestion"] = False

        return rec
