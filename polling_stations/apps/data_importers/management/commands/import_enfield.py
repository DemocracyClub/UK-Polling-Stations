from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENF"
    addresses_name = (
        "2022-05-05/2022-03-01T15:41:50.624748/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-01T15:41:50.624748/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # Enfield Highway Community Centre, 117 Hertford Road, Enfield
        if record.polling_place_id == "8115":
            record = record._replace(polling_place_easting="535189")
            record = record._replace(polling_place_northing="197091")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "207017770",  # 293A HERTFORD ROAD, ENFIELD
            "207016774",  # FLAT 2 928 HERTFORD ROAD, ENFIELD
        ]:
            return None

        if record.addressline6 in [
            "N14 5BU",
            "N21 2DS",
            "N9 9RP",
            "N18 2EH",
        ]:
            return None

        return super().address_record_to_dict(record)
