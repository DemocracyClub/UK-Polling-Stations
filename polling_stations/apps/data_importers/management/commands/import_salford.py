from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLF"
    addresses_name = (
        "2023-05-04/2023-03-24T11:25:53.715865/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-24T11:25:53.715865/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001037110",  # PADIHAM FARM ENGINE LANE, TYLDESLEY
            "10004682203",  # ALDERWOOD COTTAGE, LEIGH ROAD, WORSLEY, MANCHESTER
            "10095311109",  # APARTMENT 1, THORNCLIFFE, 48 VINE STREET, SALFORD
            "10090621036",  #  FLAT ABOVE 2 ST JAMES ROAD, SALFORD
            "10090621073",  # FLAT AT SWINTON PARK GOLF CLUB EAST LANCASHIRE ROAD, SWINTON
            "100012471364",  # WESTWOOD LODGE, PARRIN LANE, ECCLES, MANCHESTER
            "100011357863",  # 2A DUDLEY ROAD, CADISHEAD, MANCHESTER
            "100011424265",  # 47 VINE STREET, SALFORD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "M27 0JE",
            "M27 4BL",  # SWINTON HALL ROAD, SWINTON, MANCHESTER
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Boundary Stone, Bridgewater Road, Worsley, M28 1AD
        if record.polling_place_id == "6643":
            record = record._replace(
                polling_place_easting="372564",
                polling_place_northing="401679",
            )

        return super().station_record_to_dict(record)
