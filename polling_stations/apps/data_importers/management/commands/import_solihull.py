from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOL"
    addresses_name = "2024-07-04/2024-06-03T11:13:12.735398/SOL_combined.tsv"
    stations_name = "2024-07-04/2024-06-03T11:13:12.735398/SOL_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "10095758833",  # ORCHARD BARN, WOOTTON LANE, BALSALL COMMON, COVENTRY
            "200003832494",  # MARSH HOUSE FARM, MARSH HOUSE FARM LANE, BRADNOCKS MARSH, SOLIHULL
            "200003834342",  # TOBY CARVERY, COVENTRY ROAD, MERIDEN, COVENTRY
            "10008211147",  # ANNEXE EASTCOTE CORNER FRIDAY LANE, BARSTON, SOLIHULL
            "100071342190",  # COACH HOUSE, ELMDON PARK, SOLIHULL
            "100070956066",  # 1 ST. JOHNS GROVE, BIRMINGHAM
            "100071341544",  # WILLOW COTTAGE, WOOTTON LANE, BALSALL COMMON, COVENTRY
            "10090948740",  # MANAGERS FLAT BIRMINGHAM DOGS HOME CATHERINE DE BARNES LANE, CATHERINE DE BARNES
        ]:
            return None

        if record.addressline6 in [
            # split
            "B37 7RN",
            "B92 8NA",
            "B90 3QQ",
            "B36 0QB",
            "B93 8PP",
            "B90 4DP",
            # suspect
            "B90 8BW",  # BLYTHE VALLEY PARK, SHIRLEY, SOLIHULL
            "B90 4FG",  # SHIRLEY, SOLIHULL
            "B90 8BW",  # DARBY CLOSE, BLYTHE VALLEY
            "CV7 7PS",  # OXHAYES CLOSE, BALSALL COMMON, COVENTRY
            "CV7 7SZ",  # WELLFIELD CLOSE, BALSALL COMMON, COVENTRY
            "CV7 7SF",  # WELLFIELD CLOSE, BALSALL COMMON, COVENTRY
            "CV8 1PT",  # WELLFIELD CLOSE, BALSALL COMMON, COVENTRY
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Info from council - x/y from UPRN. 5th Solihull Scouts (UPRN is 010008212576)
        if record.polling_place_id == "10961":
            record = record._replace(
                polling_place_easting="412782", polling_place_northing="279167"
            )
        # Info from council - x/y from UPRN. Elmwood Place (UPRN is 010090947819)
        if record.polling_place_id == "11158":
            record = record._replace(
                polling_place_easting="417106", polling_place_northing="289542"
            )
        # Info from council - x/y from UPRN. The Pavilion, Hockley Heath Recreation Ground (UPRN is 010008211687)
        if record.polling_place_id == "11054":
            record = record._replace(
                polling_place_easting="415489", polling_place_northing="272625"
            )
        # Info from council - x/y from UPRN. The Pavilion (Castle Bromwich Parish Council) (UPRN should be 100071459690)
        if record.polling_place_id == "11143":
            record = record._replace(
                polling_place_easting="415430", polling_place_northing="289942"
            )
        # Info from council - x/y from UPRN. Tudor Grange Leisure Centre (UPRN is 010023646733)
        if record.polling_place_id == "10947":
            record = record._replace(
                polling_place_easting="414506", polling_place_northing="279399"
            )
        # The following are coordinates from the council:
        # Portacabin (Elmdon Park Car Park), Opposite 124-140 Tanhouse Farm Road, Elmdon, Solihull B92 9EY
        if record.polling_place_id == "11169":
            record = record._replace(
                polling_place_easting="415703",
                polling_place_northing="282642",
            )
        # Marston Green Parish Hall, Elmdon Road, Marston Green B37 7BT
        if record.polling_place_id == "11004":
            record = record._replace(
                polling_place_easting="417392",
                polling_place_northing="285238",
                polling_place_uprn="200003830088",
            )
        # St Philip’s Church, Manor Road, Dorridge B93 8DX
        if record.polling_place_id == "11172":
            record = record._replace(polling_place_uprn="200003823714")

        return super().station_record_to_dict(record)
