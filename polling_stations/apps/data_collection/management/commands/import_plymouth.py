from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000026"
    addresses_name = "parl.2019-12-12/Version 1/merged.csv"
    stations_name = "parl.2019-12-12/Version 1/merged.csv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3549":
            record = record._replace(polling_place_easting="256137")
            record = record._replace(polling_place_northing="56152")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070771403",
            "10070771404",
            "100040429061",
            "100040493091",
            "100040454247",
            "100040415376",
        ]:
            return None

        if uprn in [
            "100040499172",  # PL21BY -> PL13LP : 1 Victoria Place, Plymouth
            "100040499173",  # PL21BY -> PL13LP : 2 Victoria Place, Plymouth
            "10093900686",  # PL47AB -> PL47AE : 2A Elm Road, Plymouth
            "10093900685",  # PL47AB -> PL47AE : 2B Elm Road, Plymouth
            "100040505903",  # PL71PD -> PL71UD : WOLVERWOOD FARM, Wolverwood Lane, Plymouth
            "10070770231",  # PL47BA -> PL47AE : 6A Elm Road, Plymouth
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100040407149",  # PL23BU -> PL47EF : 87A Alexandra Road, Ford, Plymouth
            "100040499172",  # 1 Victoria Place
            "100040499175",  # 5-7 Victoria Place
            "100040499173",  # 2 Victoria Place
            "10090563677",  # FLAT 2 51 UNION STREET, PLYMOUTH
        ]:
            rec["accept_suggestion"] = False

        return rec
