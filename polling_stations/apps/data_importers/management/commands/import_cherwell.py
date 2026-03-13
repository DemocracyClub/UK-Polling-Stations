from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = (
        "2026-05-07/2026-03-13T13:20:13.892713/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-13T13:20:13.892713/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10011888678",  # ARDLEY BOARDING KENNELS, BARN HOUSE, ARDLEY, BICESTER, OX27 7HP
                "10011891304",  # PADBURY LODGE, BAYNARDS GREEN, BICESTER, OX27 7SQ
                "100120799447",  # YEW TREE LODGE, SOUTHAM ROAD, BANBURY, OX16 2EW
                "10011937818",  # 209 BALMORAL AVENUE, BANBURY, OX16 0BB
                "10011937821",  # 203 BALMORAL AVENUE, BANBURY, OX16 0BB
                "10011918678",  # FLAT AT 45 HIGH STREET, BANBURY, OX16 5LA
                "10011938272",  # THE OLD MILK SHED LANGFORD PARK FARM LONDON ROAD, BICESTER
                "10011938385",  # FLAT AT 75 HIGH STREET, BANBURY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "OX16 5AW",
            "OX27 7AE",
            # looks wrong
            "OX16 1EU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "32442":
            record = record._replace(polling_place_postcode="OX25 5TF")

        return super().station_record_to_dict(record)
