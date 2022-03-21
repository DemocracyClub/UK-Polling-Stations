from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NET"
    addresses_name = (
        "2022-05-05/2022-03-21T11:45:58.853591/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-21T11:45:58.853591/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    # West End Community Centre and Library, Condercum Road's postcode is correct, but
    # the postcode centroid has been dragged east by an errant property.

    # Sandringham Road properties in Gosforth and East Denton have apparent long
    # distances due to locations being transposed across the two areas in AddressBase.
    # Will be fine as the council data is correct and we're not displaying directions
    # maps.

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NE3 1AR",
            "NE4 9NQ",
            "NE5 1QF",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
