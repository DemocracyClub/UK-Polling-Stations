from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOL"
    addresses_name = (
        "2023-05-04/2023-03-15T17:32:52.508251/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-15T17:32:52.508251/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        upnr = record.property_urn.lstrip("0")

        if upnr in [
            "10093970442",  # 35 ROSEWOOD DRIVE, BLYTHE VALLEY PARK, SHIRLEY, SOLIHULL
            "10095760630",  # 2 BROOKLANDS, SOLIHULL
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
            "B91 1UQ",
            "B92 8NA",
            "B93 8PP",
            "B90 3QQ",
            "B90 8BW",  # BLYTHE VALLEY PARK, SHIRLEY, SOLIHULL
            "B90 4FG",  # SHIRLEY, SOLIHULL
            "B37 6PE",  # COOKS LANE, BIRMINGHAM
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # 'Barston Memorial Institute, Barston Lane, Barston, Solihull, B92 0JN'
        if record.polling_place_id == "9885":
            record = record._replace(polling_place_postcode="B92 0JU")

        # 'St Clements Church, Green Lane, Corner Clevedon Avenue, Castle Bromwich, Birmingham, B36 0BX'
        if record.polling_place_id == "9795":
            record = record._replace(polling_place_postcode="B36 0BA")

        # 'KEC Church Centre, Cooks Lane, Kingshurst, Birmingham, B37 6NU'
        if record.polling_place_id == "9699":
            record = record._replace(polling_place_postcode="B37 6NP")

        # 'Whar Hall Community Centre, Whar Hall Road, Solihull, B92 0PG'
        if record.polling_place_id == "10008":
            record = record._replace(polling_place_postcode="B92 0PE")

        # 'The Royal British Legion (Knowle) Club Limited, 1611 Warwick Road, Knowle, Solihull, B93 9LF'
        if record.polling_place_id == "9776":
            record = record._replace(polling_place_postcode="B93 9LU")

        # 'Woodlands Campus, Solihull College, Auckland Drive, Smith`s Wood, Solihull, B36 0NE'
        if record.polling_place_id == "9756":
            record = record._replace(polling_place_postcode="B36 0NF")

        # 'St Peter`s Hall, Holly Lane, Balsall Common, Coventry, CV7 7EA'
        if record.polling_place_id == "9692":
            record = record._replace(polling_place_postcode="CV7 7FT")

        # Info from council - x/y from UPRN. 5th Solihull Scouts (UPRN is 010008212576)
        if record.polling_place_id == "9900":
            record = record._replace(
                polling_place_easting="412782", polling_place_northing="279167"
            )
        # Info from council - x/y from UPRN. Elmwood Place (UPRN is 010090947819)
        if record.polling_place_id == "9753":
            record = record._replace(
                polling_place_easting="417106", polling_place_northing="289542"
            )
        # Info from council - x/y from UPRN. The Pavilion, Hockley Heath Recreation Ground (UPRN is 010008211687)
        if record.polling_place_id == "9856":
            record = record._replace(
                polling_place_easting="415489", polling_place_northing="272625"
            )
        # Info from council - x/y from UPRN. The Pavilion (Castle Bromwich Parish Council) (UPRN should be 100071459690)
        if record.polling_place_id == "9790":
            record = record._replace(
                polling_place_easting="415430", polling_place_northing="289942"
            )
        # Info from council - x/y from UPRN. Tudor Grange Leisure Centre (UPRN is 010023646733)
        if record.polling_place_id == "9967":
            record = record._replace(
                polling_place_easting="414506", polling_place_northing="279399"
            )

        return super().station_record_to_dict(record)
