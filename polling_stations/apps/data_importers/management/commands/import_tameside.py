from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = (
        "2023-05-04/2023-04-12T13:11:26.820087/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T13:11:26.820087/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090073761",  # 19A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073763",  #  21A WELLINGTON STREET, ASHTON-UNDER-LYNE
            "10090073764",  # 21B WELLINGTON STREET, ASHTON-UNDER-LYNE
            "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
            "200004406539",  # FLAT 2 BANK MILL MANCHESTER ROAD, MOSSLEY
            "10093148520",  # APARTMENT 3, 1 MARY STREET, HYDE
            "10093148339",  # 15 BECKER CLOSE, DENTON, MANCHESTER
            "200004410061",  # FLAT 2 2 OLD HALL LANE, MOTTRAM
            "100012777909",  # HOPKINS FARM COTTAGE, ARLIES LANE, STALYBRIDGE
            "100012777908",  # HOPKINS COTTAGE, ARLIES LANE, STALYBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SK15 3QZ",
            "M34 7RZ",
            "OL6 9LS",
            "M43 6DG",
            "SK14 2PF",
            "M43 7ZD",
        ]:
            return None

        return super().address_record_to_dict(record)
