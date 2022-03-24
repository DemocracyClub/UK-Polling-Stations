from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAG"
    addresses_name = (
        "2022-05-05/2022-03-24T16:05:13.475089/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-24T16:05:13.475089/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093034565",  # OAK HOUSE PENNY POT LANE TO CENTRAL HOUSE FARM, HAMPSTHWAITE
        ]:
            return None

        if record.addressline6 in [
            "HG3 5QF",
            "HG2 9LJ",
            "HG1 4JW",
            "HG2 9NW",
            "YO51 9LN",
            "YO61 2RT",
        ]:
            return None

        return super().address_record_to_dict(record)
