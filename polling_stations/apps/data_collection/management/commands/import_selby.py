from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000169"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019selby.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019selby.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4929":
            # Selby Rugby Club Sandhill Lane Selby
            record = record._replace(polling_place_postcode="YO8 4JP")
        if record.polling_place_id == "4923":
            # Lady Popplewell Centre, Beechwood Close, Sherburn in Elmet, Leeds
            record = record._replace(polling_place_postcode="LS25 6HU")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "LS24 9PA",
        ]:
            return None

        if (record.addressline1, record.addressline2) == ("Rose Lodge", "Oakwood Park"):
            record = record._replace(property_urn="10093092239")

        return super().address_record_to_dict(record)
