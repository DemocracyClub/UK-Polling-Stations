from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYO"
    addresses_name = "2021-03-18T18:04:57.973413/Bucks_dedupe.tsv"
    stations_name = "2021-03-18T18:04:57.973413/Bucks_dedupe.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10092750629",  # RASSLER WOOD LODGE, HENLEY ROAD, MEDMENHAM, MARLOW
                "10033201952",  # STABLE COTTAGE, HARLEYFORD LANE, MARLOW
                "10033201817",  # TEMPLE LOCK HOUSE HARLEYFORD LANE, MARLOW
                "200000812734",  # HQ AIR COMMAND HURRICANE BUILDING RAF HIGH WYCOMBE NEW ROAD, WALTERS ASH
                "10033206646",  # CHERRY TREE COTTAGE SKIRMETT ROAD, SKIRMETT
            ]
        ):
            return None

        if record.addressline6 in ["HP12 3HP", "HP14 4UY", "RG9 6JH"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Longburrow Hall Park Lane Stokenchurch HP14 2TQ
        if record.polling_place_id == "29395":
            record = record._replace(polling_place_postcode="HP14 3TQ")

        # Abbey View Primary Academy Kennedy Avenue High Wycombe HP11 1PZ
        if record.polling_place_id == "29855":
            record = record._replace(polling_place_postcode="HP11 1BX")

        return super().station_record_to_dict(record)
