from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter

THE_STOCKADE = {
    "polling_place_id": "2781",
    "polling_place_name": "The Stockade",
    "polling_place_address_1": "Davids Way",
    "polling_place_address_2": "Hainault",
    "polling_place_address_3": "Ilford",
    "polling_place_address_4": "",
    "polling_place_postcode": "IG6 3BQ",
    "default_polling_place_id": "269",
}


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDB"
    addresses_name = (
        "2024-05-02/2024-02-20T16:50:55.903244/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-02-20T16:50:55.903244/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # changes from council:

        # OLD: All Saints Church Hall, 51 Goodmayes Lane, Ilford, IG3 9SJ
        # NEW: All Saints Church Hall, 51A Goodmayes Lane, Ilford, IG3 9PB
        if record.polling_place_id == "2801":
            record = record._replace(
                polling_place_address_1="51A Goodmayes Lane",
                polling_place_postcode="IG3 9PB",
            )

        # OLD: Hainault Baptist Church Hall, Franklyn Gardens, Ilford IG6 2UT
        # EXISTING: The Stockade, Davids Way, Hainault, Ilford IG6 3BQ
        if record.polling_place_id == "2769":
            record = record._replace(**THE_STOCKADE)
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "IG5 0FF",
        ]:
            return None

        # station change: Hainault Baptist to The Stockade
        if record.polling_place_district_reference == "FA1":
            record = record._replace(**THE_STOCKADE)

        return super().address_record_to_dict(record)
