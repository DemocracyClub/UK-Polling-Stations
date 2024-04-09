from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NLN"
    addresses_name = (
        "2024-05-02/2024-04-09T16:45:06.805129/NLC-Polling Station Data (1).csv"
    )
    stations_name = (
        "2024-05-02/2024-04-09T16:45:06.805129/NLC-Polling Station Data (1).csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "200000888905",  # LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
            "10095555254",  # THE BARN, LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
            "10095555254",  # THE BARN, LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
            "100050213509",  # REAR OF 121, MARY STREET, SCUNTHORPE
            "100051967026",  # 68A MARY STREET, SCUNTHORPE
            "200000890811",  # WAVERNEY, SUSWORTH, SCUNTHORPE
        ]:
            return None

        if record.housepostcode in [
            # split
            "DN20 0SD",
            "DN17 1SB",
            "DN15 8XL",
            "DN15 7JH",
            "DN17 4EJ",
            # suspect,
            "DN18 5BF",  # COTTINGHAM COURT, BARTON-UPON-HUMBER
            "DN16 2RX",
            "DN16 2SE",
        ]:
            return None
        return super().address_record_to_dict(record)
