from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = (
        "2026-05-07/2026-03-23T14:16:20.594694/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-23T14:16:20.594694/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
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
                "100070624346",  # 1 BRISCOE ROAD, COVENTRY
                "100070624347",  # 2 BRISCOE ROAD, COVENTRY
                "10096164089",  # FLAT 4 WHEELWRIGHT LANE, COVENTRY
                "100070617832",  # 503 BEAKE AVENUE, COVENTRY
                "100070617834",  # 505 BEAKE AVENUE, COVENTRY
                "100070666519",  # 47 KENILWORTH ROAD, COVENTRY
                "10024028287",  # STAFF BLOCK HILTON COVENTRY PARADISE WAY, COVENTRY
                "100070663871",  # 138 HUMBER AVENUE, COVENTRY
                "100070666517",  # 45 KENILWORTH ROAD, COVENTRY
                "100071321235",  # COUNDON HALL FARM, TAMWORTH ROAD, KERESLEY END, COVENTRY
                "100070679552",  # 2 MILTON STREET, COVENTRY
                "100070705753",  # 454 STONEY STANTON ROAD, COVENTRY
                "100071517299",  # 298 FOLESHILL ROAD, COVENTRY
                "10024620550",  # 3 CURLEW CLOSE, ALDERMANS GREEN, COVENTRY
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "CV3 5DU",
            "CV6 5NU",
            "CV1 4DZ",
            "CV5 9AP",
            "CV4 9JB",
            "CV4 9LP",
            "CV2 5FN",
            # looks wrong
            "CV5 7BX",
        ]:
            return None

        return super().address_record_to_dict(record)
