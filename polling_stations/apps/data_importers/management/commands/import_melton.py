from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MEL"
    addresses_name = (
        "2024-05-02/2024-02-23T09:32:15.458646/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-23T09:32:15.458646/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # corrections from council:
        # The Old School, 4 Main Street, Muston, Nottingham
        if record.polling_place_id == "2694":
            record = record._replace(
                polling_place_uprn="100030550160",
                polling_place_easting="482883",
                polling_place_northing="337945",
                polling_place_postcode="NG13 0FB",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "100032044579",  # GLEBE FARM, MAIN STREET, SAXELBY, MELTON MOWBRAY
            "200001041532",  # HOMESTEAD COTTAGE, WALTHAM ROAD, THORPE ARNOLD, MELTON MOWBRAY
        ]:
            return None
        if record.addressline6 in [
            # split
            "NG32 1QG",
            "LE14 2XB",
            "NG32 1QQ",
            # not sure
            "LE14 4SS",
            "LE14 4SR",
        ]:
            return None

        return super().address_record_to_dict(record)
