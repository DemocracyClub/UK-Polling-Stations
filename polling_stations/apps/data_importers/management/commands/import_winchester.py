from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = "2021-04-16T14:39:51.352187/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-16T14:39:51.352187/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060590951",  # THE WHITE COTTAGE, DUNDRIDGE LANE, BISHOPS WALTHAM, SOUTHAMPTON
            "200000179223",  # PADDOCK HOUSE GALLEY DOWN FARM, DUNDRIDGE LANE, BISHOPS WALTHAM, SOUTHAMPTON
            "100062525886",  # GALLEY DOWN FARM, DUNDRIDGE LANE, BISHOPS WALTHAM, SOUTHAMPTON
        ]:
            return None

        if record.addressline6 in [
            "SO24 0PD",
            "SO24 0QA",
            "SO21 1JR",
            "SO21 2BN",
            "SO32 1HP",
            "SO23 7JX",
            "SO24 9HZ",
            "SO21 2EG",
            "SO32 2JR",
            "SO32 3PJ",
            "SO21 1FD",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Upham New Millennium Village Hall (Cttee Room)
        if record.polling_place_id == "9135":
            record = record._replace(polling_place_easting="452220")
            record = record._replace(polling_place_northing="119570")

        return super().station_record_to_dict(record)
