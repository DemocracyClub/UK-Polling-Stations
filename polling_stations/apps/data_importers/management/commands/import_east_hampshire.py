from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHA"
    addresses_name = "2023-05-04/2023-03-07T10:50:00.297753/Democracy_Club__04May2023 East Hampshire.TSV"
    stations_name = "2023-05-04/2023-03-07T10:50:00.297753/Democracy_Club__04May2023 East Hampshire.TSV"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "1710037869",  # BRIDGE MILL, MILL LANE, PETERSFIELD
            "10094122558",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
            "10032905833",  # ANNEXE THE HOPKILN FRITH END ROAD, FRITH END, BORDON
            "10094123612",  # WATERCRESS COTTAGE, STATION ROAD, BENTLEY, FARNHAM
            "10094123611",  # TWEENWAYS STATION ROAD, BENTLEY, FARNHAM
            "10094121538",  # THE STABLES, COLDREY FARM, LOWER FROYLE, ALTON
            "10094121960",  # DUNSTON HOUSE, GREEN BARN FARM, SELBORNE ROAD, ALTON
            "10094121961",  # GRAFTON HOUSE, GREEN BARN FARM, SELBORNE ROAD, ALTON
            "10094121962",  # HARDWICKE HOUSE, GREEN BARN FARM, SELBORNE ROAD, ALTON
            "1710038033",  # KILN COTTAGE, HONEY LANE, SELBORNE, ALTON
            "1710037987",  # AJAX, HONEY LANE, SELBORNE, ALTON
            "10009812215",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
            "10094122454",  # LUMBRY BARN, SELBORNE ROAD, ALTON
            "10094121982",  # TREESIDE VIEW, THE SHRAVE, FOUR MARKS, ALTON
            "10094122454",  # LUMBRY BARN, SELBORNE ROAD, ALTON
            "10094123735",  # OAK LODGE, SELBORNE ROAD, ALTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "GU33 7BB",
            "GU30 7QL",
            "PO8 0QR",
        ]:
            return None

        return super().address_record_to_dict(record)
