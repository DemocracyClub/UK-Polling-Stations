from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SDE"
    addresses_name = (
        "2023-05-04/2023-04-20T10:35:14.553119/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-20T10:35:14.553119/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091583505",  # LONG MEADOW, GRANGEWOOD, NETHERSEAL, SWADLINCOTE
            "10023236472",  # COPSWOOD, GRANGEWOOD, NETHERSEAL, SWADLINCOTE
            "200003151264",  # WILLOW COTTAGE GRANGEWOOD, GRANGEWOOD, SWADLINCOTE
            "10094711751",  # 40 APPLEBY CLOSE, LITTLEOVER, DERBY
            "10094711760",  # 25 APPLEBY CLOSE, LITTLEOVER, DERBY
            "10091583496",  # SALT COTTAGE HEATH LANE, BOUNDARY, SWADLINCOTE
            "10091581856",  # 49 ASHBY ROAD, WOODVILLE, SWADLINCOTE
            "10091581857",  # 51 ASHBY ROAD, WOODVILLE, SWADLINCOTE
            "200001489411",  # STABLE LODGE, TWYFORD ROAD, BARROW-ON-TRENT, DERBY
            "10091582711",  # 1 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582715",  # 5 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582720",  # 11 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582712",  # 2 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582714",  # 4 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582716",  # 6 SANDGATE ROAD, CHELLASTON, DERBY
            "10091582718",  # 8 SANDGATE ROAD, CHELLASTON, DERBY
            "10012010331",  # BONDWOOD BARN UNNAMED ROAD FROM BROOK STREET AND GREYSICH LANE TO FAIRVIEW FARM
            "100032026593",  # WATERWORKS HOUSE, DERBY ROAD, STANTON-BY-BRIDGE, DERBY
            "100030238970",  # 1 MARSTON LANE, HATTON, DERBY
            "100030231955",  # 2 NEWTON MOUNT COTTAGES, BRETBY LANE, BRETBY, BURTON-ON-TRENT
            "100032244975",  # WEBB COURT, PARK ROAD, OVERSEAL, SWADLINCOTE
            "10000820723",  # SALTERSFORD HOUSE, EGGINTON, DERBY
            "200003154106",  # BIRCHTREES FARM, EGGINTON, DERBY
            "10094713650",  # 46 SWARTLING DRIVE, WOODVILLE, SWADLINCOTE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DE65 6LE",
            "DE11 0DQ",
            "DE3 0AX",  # KINGLAS DRIVE, MICKLEOVER, DERBY
            "DE6 5JF",  # SUTTON-ON-THE-HILL, ASHBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station Mobile Unit (6211) is in Derby City Council (DER)
        # Checked and no action required, it is a mobile station close to the council border
        return super().station_record_to_dict(record)
