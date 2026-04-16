from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KHL"
    addresses_name = (
        "2026-05-07/2026-03-16T13:33:33.401624/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T13:33:33.401624/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10091482471",  # 332C SOUTHCOATES LANE, KINGSTON UPON HULL, HU9 3TR
                "10091482470",  # 332B SOUTHCOATES LANE, KINGSTON UPON HULL, HU9 3TR
                "10094916505",  # FLAT 4-5 COELUS STREET, KINGSTON UPON HULL, HU9 1AX
                "10024643735",  # CLUSTER 3 THE CROSSINGS 55 GREAT UNION STREET, KINGSTON UPON HULL, HU9 1AG
                "21133711",  # FLAT OVER 19 18-19 WITHAM, KINGSTON UPON HULL
                "21133712",  # FLAT OVER 121 121-127 WITHAM, KINGSTON UPON HULL
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "HU5 5NT",
            "HU5 2RH",
            # looks wrong
            "HU9 1AT",
            "HU9 5FP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # council change for: The Abbey Hotel, 141 Coronation Road North, Hull, HU5 5QP
        if record.polling_place_id == "17297":
            record = record._replace(
                polling_place_name="Priory Baptist Church",
                polling_place_address_1="Hotham Road South",
                polling_place_postcode="HU5 5RN",
            )

        return super().station_record_to_dict(record)
