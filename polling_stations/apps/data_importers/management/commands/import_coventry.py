from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = (
        "2024-07-04/2024-06-06T15:00:02.096694/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T15:00:02.096694/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10094852156",  # 1 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852157",  # 2 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852158",  # 3 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852159",  # 4 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852160",  # 5 MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852161",  # 6A MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "10094852162",  # 6B MATHS HOUSE HALLS OF RESIDENCE GIBBET HILL ROAD, COVENTRY
                "100070642497",  # 112 DUNCROFT AVENUE, COVENTRY
                "100071316506",  # CHURCH FARM, CHURCH LANE, EASTERN GREEN, COVENTRY
                "100071316511",  # THE COTTAGE, CHURCH LANE, EASTERN GREEN, COVENTRY
                "100070624346",  # 1 BRISCOE ROAD, COVENTRY
                "100070624347",  # 2 BRISCOE ROAD, COVENTRY
                "100070659202",  # 1 HEN LANE, COVENTRY
                "10096164089",  # FLAT 4 WHEELWRIGHT LANE, COVENTRY
                "100070617832",  # 503 BEAKE AVENUE, COVENTRY
                "100070617834",  # 505 BEAKE AVENUE, COVENTRY
                "100070642497",  # 112 DUNCROFT AVENUE, COVENTRY
                "10024028309",  # FLAT ABOVE THE COCKED HAT HOTEL BRANDON ROAD, COVENTRY
                "100070666519",  # 47 KENILWORTH ROAD, COVENTRY
                "10024028287",  # STAFF BLOCK HILTON COVENTRY PARADISE WAY, COVENTRY
                "10014008379",  # CROSS POINT BREWERS FAYRE, GIELGUD WAY, CROSS POINT BUSINESS PARK, COVENTRY
                "100070663871",  # 138 HUMBER AVENUE, COVENTRY
                "100070666517",  # 45 KENILWORTH ROAD, COVENTRY
                "100071321235",  # COUNDON HALL FARM, TAMWORTH ROAD, KERESLEY END, COVENTRY
                "100070707551",  # 180 SWAN LANE, COVENTRY
                "100070707550",  # 178 SWAN LANE, COVENTRY
                "100070707549",  # 176 SWAN LANE, COVENTRY
                "100071367506",  # 239 WALSGRAVE ROAD, COVENTRY
                "100070679552",  # 2 MILTON STREET, COVENTRY
                "100070705753",  # 454 STONEY STANTON ROAD, COVENTRY
                "100071517299",  # 298 FOLESHILL ROAD, COVENTRY
                "100071367655",  # A P S ACCOUNTANT (UK) LTD, 204 WINSFORD AVENUE, COVENTRY
                "100071319758",  # SPRINGFIELD FARM, PENNY PARK LANE, COVENTRY
                "100071319757",  # SPRINGFIELD COTTAGE, PENNY PARK LANE, COVENTRY
                "100071504282",  # THE NEW TIGER MOTH, QUORN WAY, BINLEY, COVENTRY
                "10024029583",  # FLAT ABOVE THE TIGER MOTH PUBLIC HOUSE QUORN WAY, COVENTRY
                "100071316507",  # NEW HOME FARM, CHURCH LANE, EASTERN GREEN, COVENTRY
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "CV2 5FN",
            "CV4 9JB",
            "CV4 9LP",
            "CV6 5NU",
            "CV4 8GB",
            "CV6 2PY",
            "CV3 5DU",
            "CV2 1FX",
        ]:
            return None

        return super().address_record_to_dict(record)
