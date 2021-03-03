from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHA"
    addresses_name = "2021-02-23T13:32:44.471977/Democracy_Club__06May2021.tsv"
    stations_name = "2021-02-23T13:32:44.471977/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "1710037869",  # MIDDLEMARCH, BORDEAN, PETERSFIELD
            "10094122558",  # HARDWICKE HOUSE, GREEN BARN FARM, SELBORNE ROAD, ALTON
            "10094122499",  # BRIDGE MILL, MILL LANE, PETERSFIELD
            "10094121960",  # 23 PHOENIX ROAD, BORDON
            "10094121962",  # KILN COTTAGE, HONEY LANE, SELBORNE, ALTON
            "1710038033",  # AJAX, HONEY LANE, SELBORNE, ALTON
            "10094121961",  # DUNSTON HOUSE GREEN BARN FARM SELBORNE ROAD, SELBORNE, ALTON
            "1710037987",  # GRAFTON HOUSE GREEN BARN FARM SELBORNE ROAD, SELBORNE, ALTON
            "10009812215",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
        ]:
            return None

        if record.addressline6 in ["GU30 7QL", "PO8 0QR"]:
            return None

        return super().address_record_to_dict(record)
