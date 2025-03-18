from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STO"
    addresses_name = (
        "2025-05-01/2025-03-18T20:23:39.349792/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-18T20:23:39.349792/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # add point for: Pavillion in the Park, Victory Park, Cashes Green, GL5 4JE
        if record.polling_place_id == "20793":
            record = record._replace(polling_place_easting="382911")
            record = record._replace(polling_place_northing="204929")

        # add point for: Stone Village Hall, Lower Stone Lane, Stone, GL13 9LE
        if record.polling_place_id == "20864":
            record = record._replace(polling_place_easting="368339")
            record = record._replace(polling_place_northing="195210")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200003108372",  # 5 WORKMANS CLOSE, DURSLEY
                "100120525233",  # THE FORMER TELEPHONE EXCHANGE, BATH ROAD, HARDWICKE, GLOUCESTER
                "10014280441",  # FLAT FAGINS STEAKHOUSE STROUD ROAD, BROOKTHORPE, GLOUCESTER
                "10094463969",  # 1 WYNSTONES DRIVE, BROOKTHORPE, GLOUCESTER
                "100120529784",  # BROADRIDGE GREEN, HARESFIELD LANE, EDGE, STROUD
                "200003110822",  # HILLESLEIGH HOUSE, FRITHWOOD, BROWNSHILL, STROUD
                "100121257583",  # FOURWAYS BUNGALOW, MIDDLE HILL, CHALFORD HILL, STROUD
                "10090802788",  # STUDIO FLAT SOUTHANGER FARM MARLEY LANE, CHALFORD, STROUD
                "100120528842",  # TAPANUI, COWCOMBE LANE, CHALFORD, STROUD
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "GL5 4NY",
            "GL5 3JL",
            "GL5 1RG",
            # looks wrong:
            "GL6 8QP",
            "GL11 5ND",
        ]:
            return None

        return super().address_record_to_dict(record)
