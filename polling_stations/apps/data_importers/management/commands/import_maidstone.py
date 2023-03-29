from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2023-05-04/2023-03-20T09:56:08.168950/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-20T09:56:08.168950/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022893205",  # CONIFER FARM, EMMET HILL LANE, LADDINGFORD, MAIDSTONE
            "200003661383",  # THE CHERRIES, FORGE LANE, YALDING, MAIDSTONE
            "200003722582",  # COTTON WOOD, FORGE LANE, YALDING, MAIDSTONE
        ]:
            return None
        if record.addressline6 in [
            # look wrong
            "ME18 5EG",
            "ME18 5EF",
            "ME18 5ED",
        ]:
            return None  #  split
        return super().address_record_to_dict(record)
