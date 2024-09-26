from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIH"
    addresses_name = (
        "2022-05-05/2022-03-30T15:46:52.082161/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-30T15:46:52.082161/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Low Row and Feetham Literary Institute, Low Row
        if record.polling_place_id == "8204":
            # location source: https://www.richmondshire.gov.uk/media/10639/low-row-and-feetham-literary-institute.pdf
            # postcode from AddressBase
            record = record._replace(
                polling_place_postcode="DL11 6NA",  # was DL10 6NA
                polling_place_uprn="10012783785",
            )

        # 'Cleasby and Stapleton Village Hall, Cleasby,  ' (id: 7527)
        if record.polling_place_id == "8063":
            record = record._replace(polling_place_postcode="DL2 2RA")

        # 'Colburn Village Hall, Colburn Lane, Colburn, DL9 4LS' (id: 7558)
        if record.polling_place_id == "8004":
            record = record._replace(polling_place_postcode="DL9 4LZ")

        # 'North Cowton Village Hall, North Cowton, Northallerton, DL7 0HR' (id: 7569)
        if record.polling_place_id == "8075":
            record = record._replace(polling_place_postcode="DL7 0HF")

        # 'Eppleby Village Hall, Chapel Row, Eppleby, DL11 7AP' (id: 7661)
        if record.polling_place_id == "8111":
            record = record._replace(polling_place_postcode="DL11 7AU")

        # 'Aysgarth Village Hall, Main Street, Aysgarth, DL8 3AH' (id: 7515)
        if record.polling_place_id == "8158":
            record = record._replace(polling_place_postcode="DL8 3AD")

        # 'Bainbridge Village Hall, Bainbridge,  ' (id: 7519)
        if record.polling_place_id == "8162":
            record = record._replace(polling_place_postcode="DL8 3EF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "DL9 4NN",
            "DL11 6RE",
            "DL8 4LY",
            "DL8 4AS",
            "DL10 7AZ",
            "DL10 4TJ",
            "DL9 4RT",
            "DL8 4DY",
            "DL8 3AQ",
            "DL9 4JA",
            "DL10 4SN",
            "DL8 4DH",
            "DL12 9UA",
            "DL11 6NT",
            "DL8 3EA",
            "DL9 3NJ",
            "DL11 7AE",
            "DL10 7ES",
            "DL9 4LA",
        ]:
            return None

        if record.addressline6 in [
            "DL11 6NL",  # split between three; oddly placed
            "DL10 5EY",  # coincident properties; different stations
        ]:
            return None

        uprn = record.property_urn.lstrip("0")
        if (
            uprn
            in [
                "10004781106",  # CALVERTS NOOK, THE GAITS, GAYLE, HAWES
                "10034645690",  # SAUNDERS HOUSE FARM SCOTCH CORNER TO APPLEBY TRUNK ROAD, EAST LAYTON
                "100051959949",  # GARDENERS COTTAGE RICHMOND ROAD, HIPSWELL
            ]
        ):
            return None

        return super().address_record_to_dict(record)
