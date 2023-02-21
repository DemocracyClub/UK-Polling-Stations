from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWL"
    addresses_name = "2021-04-16T11:45:50.143865/North West Leicestershire Democracy_Club__06May2021 (2).tsv"
    stations_name = "2021-04-16T11:45:50.143865/North West Leicestershire Democracy_Club__06May2021 (2).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003503741",  # OLD FARMHOUSE, NOTTINGHAM ROAD, STAUNTON HAROLD, ASHBY-DE-LA-ZOUCH
            "100030573013",  # THE OLD SLAUGHTER HOUSE, PARK LANE FARM, PARK LANE, CASTLE DONINGTON, DERBY
        ]:
            return None

        if record.addressline6 in [
            "LE65 2RF",
            "DE74 2DE",
            "DE11 8HB",
            "LE67 6HP",
            "LE12 9TB",
            "LE67 5DJ",
            "DE12 6DW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Hall Lane Methodist Church Hall Lane Whitwick LE67 5FD
        if record.polling_place_id == "4013":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
