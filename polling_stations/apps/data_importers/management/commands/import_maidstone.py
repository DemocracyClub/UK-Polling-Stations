from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2021-03-23T12:00:12.575638/Maidstone Democracy_Club__06May2021.tsv"
    )
    stations_name = "2021-03-23T12:00:12.575638/Maidstone Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003731812",  # LITTLE MAGPIE FARM WHITE HILL ROAD, DETLING
            "200003726116",  # CARAVAN SQUIRREL LODGE RUMSTEAD LANE, STOCKBURY
            "200003731685",  # MOBILE HOME 2 THE GLEN PITT ROAD, KINGSWOOD
            "10022893205",  # CONIFER FARM, EMMET HILL LANE, LADDINGFORD, MAIDSTONE
            "10014308569",  # KENT AND MEDWAY NHS AND SOCIAL CARE PARTNERSHIP, TREVOR GIBBENS UNIT HERMITAGE LANE, MAIDSTONE
        ]:
            return None

        if record.addressline6 in [
            "ME17 3SW",
            "ME7 3JW",
            "ME15 0PN",
            "ME17 1DG",
            "ME17 1LG",
            "ME17 2DN",
            "ME17 2AH",
            "ME18 6AT",
            "TN12 9NZ",
            "ME15 9RA",
            "ME17 3XW",
            "ME17 3XX",
            "ME17 3XT",
            "ME17 3XY",
            "ME17 3XU",
            "ME17 3XS",
            "ME16 0WA",
            "ME16 0FU",
            "ME17 4EF",
        ]:
            return None

        return super().address_record_to_dict(record)
