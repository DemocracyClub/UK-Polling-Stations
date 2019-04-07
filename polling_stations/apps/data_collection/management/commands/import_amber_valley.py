from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000032"
    addresses_name = "local.2019-05-02/Version 1/Polling Districts 2019.csv"
    stations_name = "local.2019-05-02/Version 1/polling station data 2019.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        # most of these UPRNs are junk
        if uprn.endswith("00000000000"):
            rec["uprn"] = ""

        if uprn in [
            "10013422570",  # DE44GX -> DE45GX : Annexe At Westfields, Plaistow Green Road, Plaistow Green, Matlock, Derbyshire
            "10013424742",  # DE560HJ -> DE560HL : The Olde Barn, Morrell Wood Farm, Over Lane, Openwoodgate, Belper, Derbyshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10000253527",  # DE58JJ -> DE222NJ : 6 Poppyfields, Marehay, Ripley, Derbyshire
            "10000252922",  # DE225JL -> DE225LF : Gothic Temple, Cumberhills Road, Kedleston, Derby, Derbyshire
        ]:
            rec["accept_suggestion"] = False

        return rec
