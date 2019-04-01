from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000041"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019exe.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019exe.CSV"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "EX5 4BH":
            return None

        if uprn == "10094201363":
            rec["postcode"] = "EX1 2FS"
            rec["accept_suggestion"] = False

        if uprn in [
            "10091473785",  # EX46PH -> EX43HY : Second Floor Flat, 93 - 94 Sidwell Street, Exeter
            "10013048447",  # EX47AB -> EX47AD : Ground Floor Flat B, 12 Mount Pleasant Road, Exeter
            "100040222859",  # EX49HE -> EX49HD : 47 Main Road, Exeter
            "10091471483",  # EX13SL -> EX13WX : 62 Langaton Lane, Exeter
            "10091472405",  # EX13FL -> EX13FX : 18 St Nicholas Close, Exeter, Devon
            "10091472874",  # EX13RX -> EX13WX : 11 Monkerton Drive, Exeter
            "10023117514",  # EX44FJ -> EX42AF : Flat 1, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117516",  # EX44FJ -> EX11JA : Flat 3, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117517",  # EX44FJ -> EX11JA : Flat 4, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117518",  # EX44FJ -> EX11JA : Flat 5, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117519",  # EX44FJ -> EX11JA : Flat 6, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117520",  # EX44FJ -> EX11JA : Flat 7, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117521",  # EX44FJ -> EX11JA : Flat 8, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117522",  # EX44FJ -> EX11JA : Flat 9, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117523",  # EX44FJ -> EX11JA : Flat 10, Shirehampton House, 35-37 St David`s Hill, Exeter
            "10023117532",  # EX11JA -> EX44DZ : Flat 2, 8 Palace Gate, Exeter
            "10091473874",  # EX28EZ -> EX30FB : 24 Brewers Court, Willeys Avenue, Exeter
            "10023124557",  # EX27PF -> EX27PU : 8 Bishops Way, Exeter, Devon
            "10091473945",  # EX27PF -> EX27PU : 62 Bishops Way, Exeter, Devon
            "10023124655",  # EX27PR -> EX27PW : 61 Woodland Drive, Exeter, Devon
            "10023124717",  # EX27PS -> EX27PX : 38 Woodland Drive, Exeter, Devon
            "10091472665",  # EX27GZ -> EX27PF : 11 Harvest Lane, Exeter, Devon
            "10091472753",  # EX27NS -> EX27PR : 8 Savoy Street, Exeter, Devon
            "10091472808",  # EX27PX -> EX27SD : 2 Ken May Mews, Exeter, Devon
            "10091472813",  # EX27RN -> EX27SD : 2 Cheffers Mews, Exeter, Devon
        ]:
            rec["accept_suggestion"] = False

        return rec
