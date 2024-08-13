from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NOR"
    addresses_name = (
        "2021-03-16T10:03:50.810252/Northampton Democracy_Club__06May2021.CSV"
    )
    stations_name = (
        "2021-03-16T10:03:50.810252/Northampton Democracy_Club__06May2021.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "15055929",  # ROOM 1 115 ADNITT ROAD, NORTHAMPTON
                "15128512",  # 12 SPENCER HAVEN, NORTHAMPTON
                "15118901",  # BLOCK H ROOM 2 CHARLES BRADLAUGH HALL BOUGHTON GREEN ROAD, NORTHAMPTON
                "15061130",  # 13 SPENCER HAVEN, NORTHAMPTON
                "15055659",  # 11 SPENCER HAVEN, NORTHAMPTON
                "15055658",  # 1 ST. JOHNS WALK, WELLINGBOROUGH ROAD, NORTHAMPTON
                "15135046",  # FLAT 2A 115 COLWYN ROAD, NORTHAMPTON
                "15055656",  # BROTHER SOLUTIONS, UNIT F70, HARVEST STUDIOS, CHAPEL PLACE, NORTHAMPTON
                "15086802",  # 4 WESTERN VIEW, NORTHAMPTON
                "15129284",  # FLAT 4 LADY ANN COURT 69 EDITH STREET, NORTHAMPTON
                "15122752",  # THE WHEATSHEAF, 126 DALLINGTON ROAD, NORTHAMPTON
                "15055657",  # 14 SPENCER HAVEN, NORTHAMPTON
                "15089940",  # FIRST FLOOR FLAT 177 ADNITT ROAD, NORTHAMPTON
                "15086772",  # FLAT THE SIXFIELDS HUNGRY HORSE WALTER TULL WAY, NORTHAMPTON
            ]
        ):
            return None

        if record.addressline6 in [
            "NN1 2NQ",
            "NN2 7JP",
            "NN1 4QW",
            "NN4 8JS",
            "NN3 8NU",
            "NN4 6FA",
            "NN3 9DS",
            "NN2 7RE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mobile Unit, Local Centre Car Park Bordeaux Close Off Weggs Farm Road Alsace Park Northampton NN5 6YR
        if record.polling_place_id == "7532":
            record = record._replace(polling_place_easting="470878")
            record = record._replace(polling_place_northing="262275")

        # The Liburd Rooms Corner of Whilton Road / Holdenby Road Kingsthorpe Northampton NN2 7SB
        if record.polling_place_id == "7433":
            record = record._replace(polling_place_easting="475960")
            record = record._replace(polling_place_northing="263722")

        return super().station_record_to_dict(record)
