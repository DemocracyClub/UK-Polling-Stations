from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2024-07-04/2024-06-25T14:39:04.816838/ERY_PD_combined.csv"
    stations_name = "2024-07-04/2024-06-25T14:39:04.816838/ERY_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
                "10095588833",  # PROVENCE HOUSE, LAVENDER FIELDS, BARMBY MOOR, YORK
                "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "HU18 1EH",
            "HU10 7AD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station change from council:
        # old: MOBILE UNIT - MARTON ROAD Car Park 26 Marton Road Bridlington East Riding Of Yorkshire
        # new: : MOBILE UNIT - AMENITY LAND, PINFOLD LANE, Amenity Land, Pinfold Lane, Bridlington, YO16 7AQ
        if record.stationcode == "30":
            record = record._replace(
                add1="PINFOLD LANE",
                add2="Amenity Land",
                placename="MOBILE UNIT - AMENITY LAND",
                postcode="YO16 7AQ",
                stationcode="30",
                xordinate="517607.13",
                yordinate="468293.28",
            )
        return super().station_record_to_dict(record)
