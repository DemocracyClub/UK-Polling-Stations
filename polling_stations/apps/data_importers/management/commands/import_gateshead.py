from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2024-05-02/2024-03-07T13:36:42.094784/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T13:36:42.094784/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100000002781",  # RIDING CHASE, NORMANS RIDING POULTRY FARM, BLAYDON-ON-TYNE
            "10024187494",  # UNIT A2 CONTRACT HOUSE WELLINGTON ROAD, DUNSTON, GATESHEAD
            "100000017168",  # 74 BENSHAM ROAD, GATESHEAD
            "100000017167",  # 72 BENSHAM ROAD, GATESHEAD
            "100000017169",  # 76 BENSHAM ROAD, GATESHEAD
            "100000034744",  # 6 HAMBLETON GREEN, GATESHEAD
            "10022984423",  # HIGH EIGHTON FARM HOUSE BLACK LANE, HARLOW GREEN, GATESHEAD
            "10022993225",  # NO WORRYS ST CUTHBERTS MEWS SIDMOUTH ROAD, CHOWDENE, GATESHEAD
            "10093488362",  # 16 BIRCH CRESCENT, BIRTLEY, CHESTER LE STREET
            "10093488193",  # 10 BIRCH CRESCENT, BIRTLEY, CHESTER LE STREET
            "10093487880",  # 5 MAPLE AVENUE, BIRTLEY, CHESTER LE STREET
            "100000074532",  # CHEVVY CHASE, PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
            "100000074529",  # 130 PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NE9 5XP",
            "NE9 6JR",
            # looks wrong
            "NE39 2EA",
            "NE10 9HL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Change requested by the council
        # Old station: The Coachman, Burnthouse Lane, Whickham, Newcastle Upon Tyne, NE16 5AW (id: 10253)
        # Replaced by: Fellside Methodist Church, Ancaster Road, Whickham, Newcastle Upon Tyne, NE16 5BJ
        if record.polling_place_id == "10253":
            record = record._replace(
                polling_place_name="Fellside Methodist Church",
                polling_place_address_1="Ancaster Road",
                polling_place_address_2="",
                polling_place_address_3="Whickham",
                polling_place_address_4="Newcastle Upon Tyne",
                polling_place_postcode="NE16 5BJ",
                polling_place_easting="",
                polling_place_northing="",
            )

        return super().station_record_to_dict(record)
