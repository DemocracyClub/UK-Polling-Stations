from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2022-05-05/2022-03-23T15:47:49.310266/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T15:47:49.310266/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Ulcombe Village Hall, Headcorn Road, Ulcombe, Maidstone
        if record.polling_place_id == "3183":
            record = record._replace(polling_place_postcode="ME17 1EB")

        # Council Correction:
        # OLD: Portacabin at Springfield House Sandling Road Maidstone ME14 2LP
        # NEW: Portacabin at Dickens Road Car Park Dickens Road Maidstone Kent ME14 2QW
        if record.polling_place_id == "3419":
            record = record._replace(
                polling_place_name="Portacabin at Dickens Road Car Park",
                polling_place_address_1="Dickens Road",
                polling_place_address_2="",
                polling_place_address_3="Maidstone",
                polling_place_address_4="Kent",
                polling_place_postcode="ME14 2QW",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "ME15 9RA",
            "ME18 6AT",
        ]:
            return None  #  split
        return super().address_record_to_dict(record)
