from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000006"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019 Beaconsfield.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019 Beaconsfield.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            record.addressline1 == "Pilgrim House"
            and record.addressline2 == "12H Packhorse Road"
        ):
            record = record._replace(property_urn="", addressline6="SL9 7QE")

        if record.addressline6 == "SL0 0AF":
            return None  # looks odd

        if uprn == "10003242337":
            record = record._replace(addressline6="SL2 5QR")

        if record.addressline6 == "SL9 0BZ":
            record = record._replace(addressline6="SL0 9BZ")

        rec = super().address_record_to_dict(record)

        if uprn in [
            "100081076380",  # SL23HW -> SL23HJ : Brook House, Templewood Lane, Stoke Poges, Slough
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100081076504",  # SL36DH -> SL36DE : Devon Court, Trenches Lane, Middle Green, Slough
            "10003236731",  # UB94HE -> UB94GY : Southlands Manor, Denham Road, Denham, Uxbridge
            "10003234581",  # SL97NS -> SL09DA : Rose Cottage, 14 Hedgerley Lane, Gerrards Cross
            "10003236730",  # UB94HE -> UB94GY : The Lodge,Southlands Manor, Denham Road, Denham, Uxbridge
            "10003236731",  # UB94HE -> UB94GY : Southlands Manor, Denham Road, Denham, Uxbridge
            "10003236726",  # UB94DQ -> UB94DG : Flat 4 The Old Mill, Oxford Road, Denham, Uxbridge
            "10003236727",  # UB94DQ -> UB94DG : Flat 6 The Old Mill, Oxford Road, Denham, Uxbridge
            "10003236729",  # UB94DQ -> UB94DG : Flat 8 The Old Mill, Oxford Road, Denham, Uxbridge
        ]:
            rec["accept_suggestion"] = False

        return rec
