from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000214"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019SurryH.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019SurryH.CSV"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061567393",  # GU195ES -> GU249PJ : 37 Oakridge, West End, Woking, Surrey
            "100062330131",  # GU166NS -> GU166HY : The Bungalow, Frimley Lodge Park, Sturt Road, Frimley Green, Camberley, Surrey
            "100061558424",  # GU152EG -> GU152EF : 45 Upper Park Road, Camberley, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001740856",  # GU166PY -> GU169NP : Holly Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "200002884455",  # GU166PY -> GU169NP : Cedar Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "100061556752",  # GU151AB -> GU151AE : Wits End, Springfield Road, Camberley, Surrey
            "10002677650",  # GU206PE -> GU206PF : Cricket Lodge,Woodcote House, Snows Ride, Windlesham, Surrey
            "200001921982",  # GU153HE -> GU153HB : 46 Academy Gate, 233 London Road, Camberley, Surrey
            "100061555236",  # GU167UJ -> GU151JN : 11 Oak Hall, Portsmouth Road, Frimley, Camberley, Surrey
            "100061555236",  # GU167UJ -> GU151JN : 17 Oak Hall, Portsmouth Road, Frimley, Camberley, Surrey
            "100061555236",  # GU167UJ -> GU151JN : 20 Oak Hall, Portsmouth Road, Frimley, Camberley, Surrey
            "10002679513",  # GU153HQ -> GU153LT : 337A London Road, Camberley, Surrey
            "100062328067",  # GU152AN -> GU152JL : Flat 7 Crawley Lodge, Crawley Ridge, Camberley, Surrey
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 == "GU24 9CG":
            return None

        return rec
