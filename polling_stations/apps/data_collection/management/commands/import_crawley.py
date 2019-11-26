from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000226"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019crawley.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019crawley.tsv"
    )
    elections = ["parl.2019-12-12/Version 1"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "RH10 3HW":
            rec["postcode"] = "RH10 3GW"

        if uprn in [
            "10024122201"  # RH110EA -> RH110AE : 50A Ifield Drive, Ifield, Crawley
        ]:
            rec["accept_suggestion"] = True

        return rec

    def get_station_point(self, record):

        # Furnace Green Community Centre
        if record.polling_place_id == "774":
            return None

        # Wakehams Green Community Centre
        if record.polling_place_id == "789":
            return None

        # Southgate West Community Centre
        if record.polling_place_id == "795":
            return None

        return super().get_station_point(record)
