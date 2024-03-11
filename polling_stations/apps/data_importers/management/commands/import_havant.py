from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = (
        "2024-05-02/2024-03-13T18:24:56.064221/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T18:24:56.064221/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060449180",  # 161A WEST LANE, HAYLING ISLAND
            "100060449181",  # 161 WEST LANE, HAYLING ISLAND
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PO9 4JG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # point correction for: Queens Inclosure Primary School, Cornelius Drive, Waterlooville, PO7 8NT
        if record.polling_place_id == "7790":
            record = record._replace(polling_place_easting="469447")
            record = record._replace(polling_place_northing="110277")

        # postcode correction for: St Wilfrid`s Lower Church Hall, Padnell Road, Waterlooville, PO8 8DJ
        if record.polling_place_id == "7850":
            record = record._replace(polling_place_postcode="PO8 8DZ")

        return super().station_record_to_dict(record)
