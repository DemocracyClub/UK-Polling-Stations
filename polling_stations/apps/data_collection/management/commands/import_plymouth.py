from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000026"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Pl.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Pl.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["100040454247", "100040412140"]:
            return None

        if uprn in [
            "100040499172",  # PL21BY -> PL13LP : 1 Victoria Place, Plymouth
            "100040499173",  # PL21BY -> PL13LP : 2 Victoria Place, Plymouth
            "10093900686",  # PL47AB -> PL47AE : 2A Elm Road, Plymouth
            "10093900685",  # PL47AB -> PL47AE : 2B Elm Road, Plymouth
            "100040505903",  # PL71PD -> PL71UD : WOLVERWOOD FARM, Wolverwood Lane, Plymouth
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10070771945",  # PL21NS -> PL22BS : FIRST FLOOR FLAT, 33 College Road, Plymouth
            "10090563020",  # PL48JA -> PL74BJ : FLAT 1, 22 Clifton Street, Plymouth
            "10090563021",  # PL48JA -> PL74BJ : FLAT 2, 22 Clifton Street, Plymouth
            "100040407149",  # PL23BU -> PL47EF : 87A Alexandra Road, Ford, Plymouth
            "10012059634",  # PL71QY -> PL99JZ : 58B Underlane, Plympton, Plymouth
        ]:
            rec["accept_suggestion"] = False

        return rec
