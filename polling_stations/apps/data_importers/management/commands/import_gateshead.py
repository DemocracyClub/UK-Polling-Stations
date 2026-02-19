from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2026-05-07/2026-02-06T07:56:31.998058/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-06T07:56:31.998058/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # station change from council:
        # old station: Low Fell Library 710a Durham Road Low Fell Gateshead NE9 6HT
        # new station: St Ninans Church, Ivy Lane, Harlow Green, NE9 6QD
        if record.polling_place_id == "12210":
            record = record._replace(
                polling_place_name="St Ninans Church",
                polling_place_address_1="Ivy Lane",
                polling_place_address_2="Harlow Green",
                polling_place_address_3="",
                polling_place_address_4="",
                polling_place_postcode="NE9 6QD",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100000002781",  # RIDING CHASE, NORMANS RIDING POULTRY FARM, BLAYDON-ON-TYNE
                "10022984423",  # HIGH EIGHTON FARM HOUSE BLACK LANE, HARLOW GREEN, GATESHEAD
                "100000074532",  # CHEVVY CHASE, PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
                "100000074529",  # 130 PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "NE10 9HL",
        ]:
            return None

        return super().address_record_to_dict(record)
