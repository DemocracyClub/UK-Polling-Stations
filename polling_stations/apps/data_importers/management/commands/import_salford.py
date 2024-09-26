from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLF"
    addresses_name = "2024-07-04/2024-05-30T15:14:43.775851/Democracy_Club__04July2024 - Salford City Council.tsv"
    stations_name = "2024-07-04/2024-05-30T15:14:43.775851/Democracy_Club__04July2024 - Salford City Council.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200001037110",  # PADIHAM FARM ENGINE LANE, TYLDESLEY
                "10004682203",  # ALDERWOOD COTTAGE, LEIGH ROAD, WORSLEY, MANCHESTER
                "10095311109",  # APARTMENT 1, THORNCLIFFE, 48 VINE STREET, SALFORD
                "10090621036",  # FLAT ABOVE 2 ST JAMES ROAD, SALFORD
                "10090621073",  # FLAT AT SWINTON PARK GOLF CLUB EAST LANCASHIRE ROAD, SWINTON
                "100012471364",  # WESTWOOD LODGE, PARRIN LANE, ECCLES, MANCHESTER
                "100011357863",  # 2A DUDLEY ROAD, CADISHEAD, MANCHESTER
                "100011424265",  # 47 VINE STREET, SALFORD
                "10095868168",  # 569 LIVERPOOL STREET, SALFORD
                "10095868167",  # 567 LIVERPOOL STREET, SALFORD
                "10095868166",  # 565 LIVERPOOL STREET, SALFORD
                "100012698449",  # ECCLES COLLEGE, CHATSWORTH ROAD, ECCLES, MANCHESTER
                "10095311112",  # APARTMENT 4, THORNCLIFFE, 48 VINE STREET, SALFORD
                "10095311110",  # APARTMENT 2, THORNCLIFFE, 48 VINE STREET, SALFORD
                "10095311111",  # APARTMENT 3, THORNCLIFFE, 48 VINE STREET, SALFORD
                "10095311117",  # APARTMENT 9, THORNCLIFFE, 48 VINE STREET, SALFORD
                "10095311120",  # APARTMENT 12, THORNCLIFFE, 48 VINE STREET, SALFORD
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "M27 0JE",
            # looks wrong
            "M27 4BL",
            "M6 8EZ",
            "M30 9RT",
            "M30 9ED",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: The Boundary Stone, Bridgewater Road, Worsley, M28 1AD
        # fixing warning: WARNING: Polling station The Boundary Stone (7196) is in Wigan Metropolitan Borough Council
        if record.polling_place_id == "8083":
            record = record._replace(
                polling_place_easting="372564",
                polling_place_northing="401679",
            )

        return super().station_record_to_dict(record)
