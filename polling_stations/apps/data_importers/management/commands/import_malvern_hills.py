from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAV"
    addresses_name = (
        "2025-05-01/2025-03-06T15:44:24.325783/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-06T15:44:24.325783/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # St Mary`s Church Hall Sherrards Green Road Malvern
        if record.polling_place_id == "15432":
            record = record._replace(
                polling_place_easting="379264",
                polling_place_northing="246303",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093062320",  # LOG CABIN AT 2 STRAWBERRY COTTAGE A443 NEWNHAM BRIDGE, NEWNHAM BRIDGE
                "10014090439",  # BAKERS COTTAGE, WICHENFORD, WORCESTER
                "10024321016",  # THE CARTHOUSE, BIRCHLEY MILL, BOCKLETON ROAD, OLDWOOD, TENBURY WELLS
                "10095597143",  # 7 CIDER MILL CLOSE, RUSHWICK, WORCESTER
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "WR14 4JY",
            "WR2 4TD",
            "WR15 8DP",
            "WR2 6RB",
            # suspect
            "WR2 4FB",
        ]:
            return None

        return super().address_record_to_dict(record)
