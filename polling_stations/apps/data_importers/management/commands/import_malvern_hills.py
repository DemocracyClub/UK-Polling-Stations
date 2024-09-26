from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAV"
    addresses_name = (
        "2024-07-04/2024-05-29T16:50:05.986897/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-29T16:50:05.986897/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # St Mary`s Church Hall Sherrards Green Road Malvern
        if record.polling_place_id == "14882":
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
                "100120595356",  # HUNTERS LODGE, MAIN ROAD, KEMPSEY, WORCESTER
                "200003222513",  # CATTERHALL FARM HOUSE, STOCKS ROAD, ALFRICK, WORCESTER
                "10014094151",  # ST. MICHAELS CARAVAN PARK, ST. MICHAELS, TENBURY WELLS
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "WR2 4TD",
            "WR2 6RB",
            "WR15 8DP",
            "WR14 4JY",
            "WR6 6BH",
            # suspect
            "WR2 5RG",
            "WR2 5GY",
            "WR2 4FB",
            "WR14 2WE",
        ]:
            return None

        return super().address_record_to_dict(record)
