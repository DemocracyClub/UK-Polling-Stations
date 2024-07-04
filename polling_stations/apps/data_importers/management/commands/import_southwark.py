from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWK"
    addresses_name = (
        "2024-07-04/2024-06-06T12:15:04.024597/Democracy_Club__04July2024_Southwark.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T12:15:04.024597/Democracy_Club__04July2024_Southwark.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # split
            "SE16 6AZ",
            "SE5 0SY",
            "SE15 6BJ",
            "SE5 7HY",
            # suspect:
            "SE24 9JQ",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station point correction from council for:
        # Thomas Calton Centre, Corner of Alpha Street and Choumert Road, London
        if record.polling_place_id == "18506":
            record = record._replace(
                polling_place_easting="534244",
                polling_place_northing="176074",
            )
        return super().station_record_to_dict(record)
