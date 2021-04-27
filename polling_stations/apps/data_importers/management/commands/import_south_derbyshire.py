from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SDE"
    addresses_name = "2021-04-16T14:48:11.190882/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-16T14:48:11.190882/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

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
            "10090303873",  # 29 WESTONHILL CHALET PARK BRIDGE LANE, WESTON ON TRENT, DERBY
            "10012010331",  # BONDWOOD BARN UNNAMED ROAD FROM BROOK STREET AND GREYSICH LANE TO FAIRVIEW FARM, HARTSHORNE, SWADLINCOTE
        ]:
            return None

        if record.addressline6 in [
            "DE65 6SL",
            "DE3 0AX",
            "DE11 9AE",
            "DE65 6LE",
            "DE65 6RG",
            "DE12 6PZ",
            "DE12 8DB",
            "DE11 0DQ",
            "DE11 0HT",
            "DE11 0TU",
            "DE65 6BP",
            "DE73 7GZ",
            "DE11 9TG",
        ]:
            return None

        return super().address_record_to_dict(record)
