from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAG"
    addresses_name = "2021-11-16T10:10:34.996455/Democracy_Club__25November2021 (1).CSV"
    stations_name = "2021-11-16T10:10:34.996455/Democracy_Club__25November2021 (1).CSV"
    elections = ["2021-11-25"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100050407904",  # GROVE HOUSE BUNGALOW, SKIPTON ROAD, HARROGATE
            "100050429604",  # HAWTHORNS, STUDLEY ROAD, RIPON
            "10093034565",  # OAK HOUSE PENNY POT LANE TO CENTRAL HOUSE FARM, HAMPSTHWAITE
        ]:
            return None

        if record.addressline6 in [
            "HG3 5QF",
            "HG3 3AT",
            "HG2 9LJ",
            "HG1 4JW",
            "HG2 9NW",
            "YO51 9LN",
        ]:
            return None

        return super().address_record_to_dict(record)
