from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000107"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-06.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-06.csv"
    )
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if not rec:
            return rec
        if rec["internal_council_id"] in [
            "54-hodsoll-street-ridley-village-hall",
            "57-fawkham-and-hartley-church-centre",
        ]:
            return None
        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.pollingstationnumber == "n/a":
            return None

        if record.houseid.strip() in ["9004672", "9004673"]:
            rec["postcode"] = "DA2 7AP"

        if uprn in [
            "10023438353",  # DA11JB -> DA11HS : Flat Above The Plough 110 Lowfield Street, Dartford, Kent
            "100060873013",  # DA28AX -> DA28DL : Beacon House Shellbank Lane, Bean, Dartford, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100060862814"  # DA99XT -> DA13JB : 104 Havelock Drive, Greenhithe, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
