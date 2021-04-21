from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NET"
    addresses_name = "2021-04-08T11:07:29.855297/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-08T11:07:29.855297/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    # West End Community Centre and Library, Condercum Road's postcode is correct, but
    # the postcode centroid has been dragged east by an errant property.

    # Sandringham Road properties in Gosforth and East Denton have apparent long
    # distances due to locations being transposed across the two areas in AddressBase.
    # Will be fine as the council data is correct and we're not displaying directions
    # maps.

    def address_record_to_dict(self, record):
        if record.addressline6 in ["NE3 1AR", "NE4 9NQ", "NE5 1QF", "NE2 1AA"]:
            return None  # split

        return super().address_record_to_dict(record)
