from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "EST"
    addresses_name = "2024-07-04/2024-06-25T15:10:11.622430/EST_PD_combined.csv"
    stations_name = "2024-07-04/2024-06-25T15:10:11.622430/EST_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "100031648376",  # OUSLEY CROSS FARM, STANTON LANE, ELLASTONE, ASHBOURNE
                "10008036775",  # THORSWOOD GRANGE, STANTON, ASHBOURNE
                "10008036394",  # PARKGATE COTTAGE, WOOTTON ROAD, ELLASTONE, ASHBOURNE
                "10094378229",  # DOVE CROFT BARN, BARROW HILL, ROCESTER, UTTOXETER
                "100031678921",  # 34 HOLLY ROAD, UTTOXETER
                "100031678918",  # 32 HOLLY ROAD, UTTOXETER
                "10008040309",  # NOAHS ARK FARM, BY PASS ROAD, UTTOXETER
                "100032199973",  # WOODFORD HALL FARM, MOISTY LANE, MARCHINGTON, UTTOXETER
                "10010540344",  # THE CROFT, HIGHWOOD, UTTOXETER
                "10090991258",  # LEAFIELDS BARN, LOWER LOXLEY, UTTOXETER
                "10008040504",  # REDBANK FARM, WOODMILL, YOXALL, BURTON-ON-TRENT
                "10008039588",  # STONEYFORD FARM, STONEYFORD, BARTON UNDER NEEDWOOD, BURTON-ON-TRENT
                "10008042769",  # 307 LICHFIELD ROAD, BARTON UNDER NEEDWOOD, BURTON-ON-TRENT
                "10008042692",  # GREENAWAYS, LICHFIELD ROAD, BRANSTON, BURTON-ON-TRENT
                "100031666894",  # HENESFIELD FARM, OUTWOODS LANE, BURTON-ON-TRENT
                "100031664179",  # OUTWOODS HILL FARM, LOWER OUTWOODS ROAD, BURTON-ON-TRENT
                "10008039970",  # MYRTLE COTTAGE, JARDINES LANE, STUBWOOD, UTTOXETER
                "100031649648",  # 100 ASHBY ROAD, BURTON-ON-TRENT
                "100031650804",  # 14 BEARWOOD HILL ROAD, BURTON-ON-TRENT
                "100031650805",  # 15 BEARWOOD HILL ROAD, BURTON-ON-TRENT
                "10010540757",  # 4A LODGE HILL, TUTBURY, BURTON-ON-TRENT
                "10009257620",  # OAKAMORE, ANSLOW ROAD, HANBURY, BURTON-ON-TRENT
                "10010542140",  # ANFIELD HOUSE FARM, NEW ROAD, UTTOXETER
                "100031680029",  # PARK VIEW, NEW ROAD, UTTOXETER
                "100031680026",  # ASHDENE, NEW ROAD, UTTOXETER
                "100031680035",  # THE HAVEN, NEW ROAD, UTTOXETER
                "100031678433",  # 1 HAWTHORNDEN AVENUE, UTTOXETER
                "200001719328",  # SCHOOL HOUSE, STONE ROAD, UTTOXETER
                "10008037294",  # OAKLANDS, SCOUNSLOW GREEN ROAD, SCOUNSLOW GREEN, UTTOXETER
                "100032002408",  # THREE LANE END FARM, THORNEY LANES, NEWBOROUGH, BURTON-ON-TRENT
                "100031679871",  # NEWLANDS COTTAGE FARM, MOISTY LANE, MARCHINGTON, UTTOXETER
                "10009259655",  # DOVEDALE HOUSE, CALWICH, ASHBOURNE
                "10009259632",  # WHITEHALL BANK FARM, DRAYCOTT-IN-THE-CLAY, ASHBOURNE
                "100031679871",  # NEWLANDS COTTAGE FARM, MOISTY LANE, MARCHINGTON, UTTOXETER
                "100031672646",  # OAKLANDS COTTAGE, THORNEY LANES, NEWBOROUGH, BURTON-ON-TRENT
                "100031672649",  # TOMLINSONS CORNER FARM, THORNEY LANES, NEWBOROUGH, BURTON-ON-TRENT
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "DE13 9AZ",
            "ST14 5DS",  # HAWTHORNE, NEW ROAD, UTTOXETER
            "ST14 7RB",  # HOLLYSTONE, STONE ROAD, UTTOXETER
            "DE15 0FD",  # WEST STREET, BURTON-ON-TRENT
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Giles Church, Croxden Lane, Croxden ,Uttoxeter, Staffordshire
        if record.pollingstationid == "4383":
            record = record._replace(xordinate="406486")
            record = record._replace(yordinate="339871")

        return super().station_record_to_dict(record)
