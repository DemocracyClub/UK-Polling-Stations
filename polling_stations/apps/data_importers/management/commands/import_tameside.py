from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = (
        "2022-05-05/2022-03-25T15:02:16.351806/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-25T15:02:16.351806/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn.lstrip("0") in [
            # single property too far
            "200004405547",
            # another group too far
            "10090073761",
            "10090073763",
            "10090073764",
            "100012777279",
            "200002032772",
            # embedded in another area
            "200004400819",
            "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
            "200004406539",  # FLAT 2 BANK MILL MANCHESTER ROAD, MOSSLEY
            # across another area
            "10093148014",  # 1 MEADOW VIEW GARDENS, DROYLSDEN, MANCHESTER
            "10093148018",  # 5 MEADOW VIEW GARDENS, DROYLSDEN, MANCHESTER
        ]:
            return None

        if record.addressline6 in [
            "OL6 9LS",
            "SK15 1HF",
            "M34 7RZ",
            "M43 7ZD",
        ]:
            return None  # split

        if record.addressline6 in [
            "SK14 3GD",  # embedded in another area. postcode centroid a long way from these residential properties
            "SK14 3EB",  # embedded in another area
            "SK14 3GU",  # dubious geolocation; too far; through another area
            "M34 2WS",  # embedded in another area
            "SK14 2BN",  # embedded in another area
        ]:
            return None

        return super().address_record_to_dict(record)
