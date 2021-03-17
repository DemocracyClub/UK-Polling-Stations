from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WFT"
    addresses_name = (
        "2021-03-16T10:53:30.497143/Waltham Forest Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-16T10:53:30.497143/Waltham Forest Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022565563",  # 613A LEA BRIDGE ROAD, LONDON
            "200001446803",  # 24A COURTENAY ROAD, LEYTONSTONE
            "100022554342",  # SECOND FLOOR FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "100022574998",  # 6A ST JAMES MEWS, WALTHAMSTOW
            "100022576875",  # FIRST FLOOR REAR FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "100022565551",  # SECOND FLOOR FLAT 7A ST JAMES STREET, WALTHAMSTOW
            "100022573045",  # GROUND FLOOR STUDIO FLAT 286 HIGH ROAD LEYTON, LEYTON
            "100022565559",  # FIRST FLOOR FRONT FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "10009143272",  # 22 PENNANT TERRACE, LONDON
            "100022538159",  # 311A HIGH ROAD LEYTONSTONE, LEYTONSTONE
            "100022597338",  # FLAT 1, COWLEY COURT, WEST STREET, LONDON
            "200001431268",  # 28A HOE STREET, LONDON
            "200001429422",  # 305A HIGH ROAD LEYTONSTONE, LONDON
            "100022565542",  # 277A HIGH ROAD LEYTONSTONE, LONDON
            "10009141073",  # 301A HIGH ROAD LEYTONSTONE, LONDON
            "10095403489",  # 68 MANOR ROAD, LONDON
            "10009150512",  # 42A FARMER ROAD, LONDON
            "200001429424",  # FLAT 1, 58 BORTHWICK ROAD, LONDON
            "200001452659",  # 135A HIGH ROAD LEYTON, LONDON
            "100022576731",  # 28B HOE STREET, WALTHAMSTOW
            "100022565555",  # 63C BARCLAY ROAD, LONDON
            "200001440243",  # 12 EAST AVENUE, LONDON
            "100022576877",  # 63B BARCLAY ROAD, LONDON
            "100022565565",  # 71 MACDONALD ROAD, LONDON
            "10091184386",  # 79 MACDONALD ROAD, LONDON
            "10091186606",  # 60A HIGH ROAD LEYTON, LONDON
            "100022565540",  # 59 MACDONALD ROAD, LONDON
            "10091186607",  # 83 MACDONALD ROAD, LONDON
            "200001448154",  # 63 MACDONALD ROAD, LONDON
            "100022555840",  # 67 MACDONALD ROAD, LONDON
            "100022561825",  # 57 MACDONALD ROAD, LONDON
            "100022565546",  # 73 MACDONALD ROAD, LONDON
            "10091184384",  # 77 MACDONALD ROAD, LONDON
            "100022554332",  # 65 MACDONALD ROAD, LONDON
            "100022593379",  # 69 MACDONALD ROAD, LONDON
            "100022565553",  # 81 MACDONALD ROAD, LONDON
            "100022565544",  # 61 MACDONALD ROAD, LONDON
            "100022565536",  # 75 MACDONALD ROAD, LONDON
            "200001429423",  # 85 MACDONALD ROAD, LONDON
            "10009150513",  # 4 OLIVER ROAD, LONDON
            "100022565557",  # FLAT 2, 21 ALEXANDRA ROAD, LONDON
            "10009148484",  # SECOND FLOOR FLAT 128 VICARAGE ROAD, LEYTON
            "100022565548",  # GROUND FLOOR FLAT 1 27 QUEENS ROAD, LEYTONSTONE
            "10091184385",  # FLAT 5 85 WHIPPS CROSS ROAD, LEYTONSTONE
            "100022521079",  # FIRST FLOOR FLAT 128 VICARAGE ROAD, LEYTON
            "100022565538",  # 290B HIGH ROAD LEYTON, LONDON
            "200001452011",  # MORTUARY LODGE ST PATRICKS ROMAN CATHOLIC CEMETRY 57 LANGTHORNE ROAD, LEYTONSTONE
            "10009143848",  # 55A NORLINGTON ROAD, LONDON
            "10024420779",  # FLAT B 292 HIGH ROAD LEYTON, LEYTON
            "100022535453",  # 307A HIGH ROAD LEYTONSTONE, LONDON
            "100022554345",  # 309A-311A HIGH ROAD LEYTONSTONE, LONDON
            "10024419386",  # 55 BLACKHORSE ROAD, LONDON
            "100022963336",  # 27 PENNANT TERRACE, LONDON
            "100022981619",  # 316B LEA BRIDGE ROAD, LONDON
            "10009150657",  # 316A LEA BRIDGE ROAD, LONDON
            "100022517750",  # 316C LEA BRIDGE ROAD, LONDON
            "100022565561",  # 29 PENNANT TERRACE, LONDON
            "100023696171",  # 3 OAKLANDS, 37 WEST AVENUE, LONDON
            "100022954537",  # 1A VESTRY ROAD, LONDON
            "10024419211",  # 1B VESTRY ROAD, LONDON
            "100022541463",  # 2 OAKLANDS, 37 WEST AVENUE, LONDON
            "10009142555",  # 1 OAKLANDS, 37 WEST AVENUE, LONDON
            "10009149436",  # 24 PENNANT TERRACE, LONDON
            "100022981651",  # 46A PEMBROKE ROAD, LONDON
            "10093563214",  # 120 BEULAH ROAD, LONDON
            "200001425453",  # 112 FARMILO ROAD, LONDON
            "100022599055",  # 92 WITHY MEAD, LONDON
            "100023001581",  # BAILEY GARDINER CARS LTD, 32A THE AVENUE, LONDON
            "10009148706",  # 824B LEA BRIDGE ROAD, WALTHAMSTOW
            "100022543266",  # 14 FOREST ROAD, LONDON
            "200001416768",  # 24B COURTENAY ROAD, LEYTONSTONE
        ]:
            return None

        if record.addressline6 in [
            "E17 7EA",
            "E11 3FG",
            "E17 4PE",
            "E17 4ED",
            "E17 7NE",
            "E10 5NJ",
            "E17 5EL",
            "E17 5FX",
            "E4 9DP",
            "E17 3DA",
            "E17 9NH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mission Grove (South Site) 108 Edinburgh Road Walthamstow London E17 7QB
        if record.polling_place_id == "5280":
            record = record._replace(polling_place_easting="536937")
            record = record._replace(polling_place_northing="188842")

        return super().station_record_to_dict(record)
