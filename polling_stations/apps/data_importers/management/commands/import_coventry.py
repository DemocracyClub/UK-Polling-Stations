from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = (
        "2023-05-04/2023-03-13T10:50:59.017753/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T10:50:59.017753/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095509721",  # FLAT ABOVE BROAD LANE TRADING ESTATE BANNER LANE, COVENTRY
            "10094852156",  # 1 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852157",  # 2 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852158",  # 3 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852159",  # 4 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852160",  # 5 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852161",  # 6A MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "10094852162",  # 6B MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
            "100070642497",  # 112 DUNCROFT AVENUE, COVENTRY
            "100071316506",  # CHURCH FARM, CHURCH LANE, EASTERN GREEN, COVENTRY
            "100070624346",  # 1 BRISCOE ROAD, COVENTRY
            "100070624347",  # 2 BRISCOE ROAD, COVENTRY
            "100070659202",  # 1 HEN LANE, COVENTRY
            "10096164089",  # FLAT 4 WHEELWRIGHT LANE, COVENTRY
            "100070617832",  # 503 BEAKE AVENUE, COVENTRY
            "100070617834",  # 505 BEAKE AVENUE, COVENTRY
            "100070642497",  # 112 DUNCROFT AVENUE, COVENTRY
            "100071316506",  # CHURCH FARM, CHURCH LANE, EASTERN GREEN, COVENTRY
            "10024028309",  # FLAT ABOVE THE COCKED HAT HOTEL BRANDON ROAD, COVENTRY
            "100070666519",  # 47 KENILWORTH ROAD, COVENTRY
            "100071318653",  # LENTON LANE FARM, LENTONS LANE, ALDERMANS GREEN, COVENTRY
            "10024028287",  # STAFF BLOCK HILTON COVENTRY PARADISE WAY, COVENTRY
            "10014008379",  # CROSS POINT BREWERS FAYRE, GIELGUD WAY, CROSS POINT BUSINESS PARK, COVENTRY
            "100070663871",  # 138 HUMBER AVENUE, COVENTRY
            "100070666517",  # 45 KENILWORTH ROAD, COVENTRY
            "100071321235",  # COUNDON HALL FARM, TAMWORTH ROAD, KERESLEY END, COVENTRY
            "100071316507",  # NEW HOME FARM, CHURCH LANE, EASTERN GREEN, COVENTRY
            "100070707551",  # 180 SWAN LANE, COVENTRY
            "100070707550",  # 178 SWAN LANE, COVENTRY
            "100070707549",  # 176 SWAN LANE, COVENTRY
            "100071367506",  # 239 WALSGRAVE ROAD, COVENTRY
            "100070679552",  # 2 MILTON STREET, COVENTRY
            "100070705753",  # 454 STONEY STANTON ROAD, COVENTRY
            "100071517299",  #
        ]:
            return None

        if record.addressline6 in [
            "CV2 1FX",  # splits
            "CV4 9LP",  # splits
            "CV2 2LS",  # splits
            "CV5 7JN",  # splits
            "CV2 5FN",  # splits
            "CV6 5NU",  # splits
            "CV2 4GA",  # SWAN LANE, COVENTRY
        ]:
            return None

        return super().address_record_to_dict(record)
