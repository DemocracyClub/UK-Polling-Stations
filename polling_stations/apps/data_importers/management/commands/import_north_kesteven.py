from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2025-05-01/2025-02-26T13:39:55.210699/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-26T13:39:55.210699/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NG34 9PU",  # split
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station change from council:
        # old: Little Hale, Parva House (Small Hall), Main Road, Little Hale, Sleaford NG34 9BA
        # new: Little Hale Methodist Church, Chapel Lane, Little Hale, Sleaford NG34 9BE
        if record.polling_place_id == "9836":
            record = record._replace(
                polling_place_name="Little Hale Methodist Church",
                polling_place_address_1="Chapel Lane",
                polling_place_address_2="Little Hale",
                polling_place_address_3="Sleaford",
                polling_place_address_4="",
                polling_place_postcode="NG34 9BE",
                polling_place_easting="0",
                polling_place_northing="0",
            )
        return super().station_record_to_dict(record)
