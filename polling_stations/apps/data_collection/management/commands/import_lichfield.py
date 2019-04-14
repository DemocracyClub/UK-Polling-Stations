from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000194"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Lich.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Lich.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013216157"  # WS70HZ -> WS70HT : The Coach House, Edial House Farm, Lichfield Road, Burntwood, Staffs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10002777436",  # B783TW -> B783SR : Longwood House, Drayton Manor Park, Tamworth, Staffs
            "10024113376",  # B783TW -> B783TJ : Manor Lodge, Drayton Manor Park, Tamworth, Staffs
            "10013216554",  # WS70BJ -> WS70BG : White Swan, 2 Cannock Road, Burntwood, Staffs
            "100032225996",  # WS140ET -> WS140EU : Hilton Studio, Pouk Lane, Hilton, Lichfield, Staffs
            "100031687250",  # WS70HY -> WS70HZ : Edial House, 415 Lichfield Road, Burntwood, Staffs
            "10013848296",  # WS140EN -> WS140ER : Lynn Lane Farm, Lynn Lane, Shenstone, Lichfield, Staffs
        ]:
            rec["accept_suggestion"] = False

        return rec
