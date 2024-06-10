from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAN"
    addresses_name = (
        "2024-07-04/2024-06-10T14:49:01.631956/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T14:49:01.631956/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032224228",  # 179 HEDNESFORD ROAD, HEATH HAYES, CANNOCK
            "100031633729",  # 398 RUGELEY ROAD, HEDNESFORD, CANNOCK
            "100031616437",  # 90 BRADBURY LANE, HEDNESFORD, CANNOCK
            "100031629543",  # 31 MILTON ROAD, CANNOCK
            "10008161077",  # 85A CANNOCK ROAD, CANNOCK
            "100031620076",  # SECOND FLOOR FLAT 23 CHURCH STREET, BRIDGTOWN, CANNOCK
            "10008161654",  # 10B WOLVERHAMPTON ROAD, CANNOCK
            "100032222352",  # 10A WOLVERHAMPTON ROAD, CANNOCK
            "100031628198",  # 174 LONGFORD ROAD, CANNOCK
            "100031617493",  # 22 BROWNHILLS ROAD, NORTON CANES, CANNOCK
            "10014216147",  # 121 WOOD LANE, HEDNESFORD, CANNOCK
            "100032223990",  # 57 BRINDLEY HEATH ROAD, HEDNESFORD, CANNOCK
            "100032223991",  # 58 BRINDLEY HEATH ROAD, HEDNESFORD, CANNOCK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WS12 3YG",
            "WS11 9NW",
            # look wrong
            "WS11 1LF",
            "WS11 9AD",
        ]:
            return None

        return super().address_record_to_dict(record)
