from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000193"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy Club Polling Districts EStaffs.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy Club Polling Stations EStaffs.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090989475",  # DE142LD -> DE142LA : 11B Derby Street
            "10090989276",  # DE142LD -> DE142LA : 12A Derby Street
            "10090989277",  # DE142LD -> DE142LA : 12B Derby Street
            "10023784825",  # DE142LF -> DE142LA : 19B Derby Street
            "200001156601",  # DE130PB -> DE130PA : 59 Kitling Greaves Lane
            "10009259693",  # DE130PA -> DE130PB : 64 Kitling Greaves Lane
            "200001155854",  # DE142PG -> DE142PQ : 63A Dallow Street
            "10009259859",  # DE142PQ -> DE142PG : 64 Dallow Street
            "10008040155",  # ST145BH -> ST145DN : Bank Top Farm, Leigh Lane, Bramshall
            "100031678852",  # ST145EP -> ST145AJ : Brycefields, Hollington Lane, Stramshall
            "10090989108",  # DE143FY -> DE143FZ : 19 Hornbeam Way, Branston
            "100031654750",  # DE139HE -> DE139BG : Woodside House, Church Road, Rolleston on Dove
            "10009259958",  # DE139AZ -> DE139AB : 120 Station Road, Rolleston on Dove
            "10008039393",  # DE62HE -> DE62EB : Toll Gate Cottage, Calwich, Mayfield
            "10010544282",  # DE138RZ -> DE138RY : Keepers Barn, Thorney Lanes, Newborough
        ]:
            rec["accept_suggestion"] = True

        return rec
