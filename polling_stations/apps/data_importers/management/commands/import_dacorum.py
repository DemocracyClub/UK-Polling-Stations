from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAC"
    addresses_name = (
        "2023-05-04/2023-03-10T12:47:03.450416/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T12:47:03.450416/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Nash Mills Village Hall
        if record.polling_place_id == "2277":
            record = record._replace(polling_place_easting="507211")
            record = record._replace(polling_place_northing="204366")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # split
            "HP2 4AP",
            "HP2 6JN",
            # wrong
            "HP3 9GT",
        ]:
            return None
        return rec
