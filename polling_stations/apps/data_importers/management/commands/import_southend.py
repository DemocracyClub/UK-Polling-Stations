from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = (
        "2023-05-04/2023-03-09T13:07:25.305816/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T13:07:25.305816/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7260":
            record = record._replace(
                polling_place_easting="586595", polling_place_northing="187653"
            )

        # Sandpiper Pre-school, Sandpiper Close/Kingfisher Close, Shoeburyness, SS3 9YB
        # correction for the council
        if record.polling_place_id == "7561":
            record = record._replace(
                polling_place_easting="593511", polling_place_northing="185908"
            )

        # Hinguar School, New Garrison Road, Shoeburyness, Southend-on-Sea, Essex, SS3 9FE
        # correction for the council
        if record.polling_place_id == "7414":
            record = record._replace(
                polling_place_easting="593387", polling_place_northing="184765"
            )

        # Centre Place Community Centre, 15 Prospect Close, Essex, SS1 6XY
        # correction for the council
        if record.polling_place_id == "7363":
            record = record._replace(
                polling_place_easting="589315", polling_place_northing="185206"
            )

        # Booth 1, John Wesley Hall	Belfairs Methodist Church, Eastwood Road North, Leigh-on-Sea, SS9 4NG
        # correction for the council
        if record.polling_place_id == "7331":
            record = record._replace(
                polling_place_easting="583854", polling_place_northing="187894"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SS9 1RP",
            "SS9 1LN",
            "SS3 9QH",
            "SS9 4RP",
            "SS9 1NH",
            "SS9 5EW",
            "SS9 1QY",
        ]:
            return None

        return super().address_record_to_dict(record)
