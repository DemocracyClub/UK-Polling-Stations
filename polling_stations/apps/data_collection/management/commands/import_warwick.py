from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000222"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Warwick.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Warwick.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7562":
            record = record._replace(polling_place_postcode="CV35 8JE")

        # Wasperton Village Hall, Wasperton
        if record.polling_place_id == "7232":
            record = record._replace(polling_place_postcode="CV35 8EB")
        # St. Paul's Church Hall, Leicester Street, Royal Leamington Spa
        if record.polling_place_id in ["7375", "7392"]:
            record = record._replace(polling_place_postcode="CV32 4TE")
        # Sherbourne Village Hall, Sherbourne
        if record.polling_place_id == "7225":
            record = record._replace(polling_place_postcode="CV35 8AN")
        # Lillington Nursery, Lillington Nursery & Primary School, Grange Road Entrance, Off Pound Lane, Lillington, Royal Leamington Spa
        if record.polling_place_id == "7395":
            record = record._replace(polling_place_postcode="CV32 7AG")
        # Lowsonford Village Hall, Lowsonford
        if record.polling_place_id == "7280":
            record = record._replace(polling_place_postcode="CV35 8JE")
        # Church of Jesus Christ Of Latter Day Saints, Saltisford/Birmingham Road/A425, Warwick
        if record.polling_place_id in ["7526", "7476", "7479"]:
            record = record._replace(polling_place_postcode="CV34 4TT")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023410405",  # CV346RB -> CV346RA : Leafields Farmhouse, Stratford Road, Warwick
            "100071508862",  # CV326QZ -> CV327UJ : Furzenhill Farm Bungalow, Coventry Road (Cubbington Heath), Cubbington Heath, Leamington Spa, Warwickshire
            "10013184003",  # CV345YD -> CV345YN : The Flat, The Saxon Mill, Guy`s Cliffe, Warwick, Warwickshire
            "10090529702",  # CV326QP -> CV326QR : Annexe Pear Tree Cottage, Stoneleigh Road, Blackdown, Royal Leamington Spa, Warwickshire
            "100071251405",  # CV82DB -> CV82DD : Bungalow, Kenilworth School, Leyes Lane, Kenilworth, Warwickshire
            "100071251404",  # CV82DD -> CV82DE : The Tiltyard, 25 Leyes Lane, Kenilworth, Warwickshire
            "10091559922",  # CV313SN -> CV313NS : 1 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559923",  # CV313SN -> CV313NS : 2 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559924",  # CV313SN -> CV313NS : 3 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559925",  # CV313SN -> CV313NS : 4 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559926",  # CV313SN -> CV313NS : 5 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559927",  # CV313SN -> CV313NS : 6 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559928",  # CV313SN -> CV313NS : 7 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559929",  # CV313SN -> CV313NS : 8 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559930",  # CV313SN -> CV313NS : 9 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559931",  # CV313SN -> CV313NS : 10 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559932",  # CV313SN -> CV313NS : 11 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559933",  # CV313SN -> CV313NS : 12 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559934",  # CV313SN -> CV313NS : 14 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559935",  # CV313SN -> CV313NS : 15 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559936",  # CV313SN -> CV313NS : 16 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559937",  # CV313SN -> CV313NS : 17 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559938",  # CV313SN -> CV313NS : 18 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559939",  # CV313SN -> CV313NS : 19 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559940",  # CV313SN -> CV313NS : 20 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559941",  # CV313SN -> CV313NS : 21 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "10091559942",  # CV313SN -> CV313NS : 22 Stephenson Court, Station Approach, Royal Leamington Spa, Warwickshire
            "100070256806",  # CV325TA -> CV324TA : 27 Vincent Street, Royal Leamington Spa, Warwickshire
            "10091555850",  # CV313LZ -> CV313JZ : De Luca House, 18A Queensway Trading Estate, Royal Leamington Spa, Warwickshire
            "10003785193",  # CV82JY -> CV82JX : Lark Wood, Hollis Lane, Kenilworth, Warwickshire
            "10003785258",  # CV82FE -> CV82FF : Crackley Barn, Coventry Road, Kenilworth, Warwickshire
            "10013181323",  # Warwick Cottage B930BS -> B930BP.
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100071257668"  # CV357EH -> CV357ED : Hill Farm House, Hill Farm, Birmingham Road, Hatton, Warwick
            "100070242180",  # CV312DL -> CV311DL : Flat A, 24 Clemens Street, Royal Leamington Spa, Warwickshire
            "10023410492",  # CV357AB -> CV358AB : The Cedars, Foxbrook House, Old Warwick Road (Rowington), Rowington, Warwick
        ]:
            rec["accept_suggestion"] = False

        # Lockhart Court addresses
        if uprn in [
            "10093988623",
            "10093988624",
            "10093988619",
            "10093988620",
            "10093988621",
        ]:
            rec["postcode"] = "CV32 4HQ"
            rec["accept_suggestion"] = False

        if uprn == "10091558863":
            rec["postcode"] = "CV34 7AW"
            rec["accept_suggestion"] = False

        return rec


# Unchecked so no action being taken

# "10091560672",  # CV325NY -> CV325AN : Upper Grove House, Beauchamp Hill, Royal Leamington Spa, Warwickshire
# "100070257723",  # CV311BN -> CV324HA : 61 Willes Road, Royal Leamington Spa, Warwickshire
# "10091556321",  # CV313PS -> CV339RJ : 10 The Old Library, Avenue Road, Royal Leamington Spa, Warwickshire
# "100070256927",  # CV325JG -> CV326AA : Chestnut Lodge, 26 Warwick New Road, Royal Leamington Spa, Warwickshire
# "100071253636",  # CV311HJ -> CV311HB : Weldon Lodge, 9 Farley Street, Royal Leamington Spa, Warwickshire
# "10013184066",  # CV346RE -> CV346RB : Management House, Hilton National Hotel, Longbridge, Warwick
# "100071258776",  # CV346RA -> CV346BQ : Fishers Brook, Stratford Road, Longbridge, Warwick
# "10013183688",  # CV346RE -> CV346RB : Staff Quarters, Hilton National Hotel, Longbridge, Warwick
# "10023410208",  # CV325JG -> CV325JQ : Falstaff Hotel, 16-20 Warwick New Road, Royal Leamington Spa, Warwickshire
# "100071511723",  # CV357JP -> CV357JX : Lockside, 3 Middle Lock Cottage, Birmingham Road, Hatton, Warwickshire
# "100071255677",  # CV325EZ -> CV325EY : 6 Charnwood House, 22 Portland Street, Royal Leamington Spa, Warwickshire
# "100070264064",  # CV345DS -> CV345DP : 68 Lower Cape, The Cape, Warwick
# "100071256745",  # CV325ND -> CV325NB : The Coach House, Arley Mews, Royal Leamington Spa, Warwickshire
# "10013183701",  # CV346HN -> CV346HS : Racecourse Bungalow, Hampton Street, Warwick
