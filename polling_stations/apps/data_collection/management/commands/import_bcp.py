from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000058"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019BCP.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019BCP.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "BH3 7JX":
            return None

        if uprn in ["10094069238", "10094069090", "10094069239", "10094069240"]:
            rec["postcode"] = "BH1 4EH"

        if uprn == "100040574446":
            rec["postcode"] = "BH23 7HU"

        if uprn in [
            "10013444802",  # BH51HN -> BH51NH : 3 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10013444805",  # BH51HN -> BH51NH : 6 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10013444800",  # BH51HN -> BH51NH : 1 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10013444801",  # BH51HN -> BH51NH : 2 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10013444803",  # BH51HN -> BH51NH : 4 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10013444804",  # BH51HN -> BH51NH : 5 Southlands Court, 11 Crabton Close Road, Bournemouth, Dorset
            "10024152851",  # BH63EY -> BH63BU : 1 Water Tower View, 33 Guildhill Road, Bournemouth, Dorset
            "10013446042",  # BH44AJ -> BH48AJ : 5 The Clarens, 4 Clarendon Road, Bournemouth, Dorset
            "10090822168",  # BH11NF -> BH14NF : Ground Floor Flat, 148 Ashley Road, Bournemouth, Dorset
            "10024395891",  # BH89RL -> BH89QG : First Floor Flat, 170 Charminster Road, Bournemouth, Dorset
            "100041108773",  # BH63BJ -> BH63BD : Ground Floor Flat, 265 Belle Vue Road, Bournemouth, Dorset
            "10024391305",  # BH51DL -> BH51HA : Boscombe Reef Hotel, 15 Westby Road, Bournemouth, Dorset
            "10023869526",  # BH13EB -> BH13DN : Carlton Hotel, Meyrick Road, Bournemouth, Dorset
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10023691209",  # BH154LZ -> BH165BJ : 47 Rockley Vale, Rockley Park, Napier Road, Poole, Dorset
            "10023691244",  # BH154LZ -> BH165BJ : 14 Lytchett Bay View, Rockley Park, Napier Road, Poole, Dorset
            "10023691479",  # BH154LZ -> BH165BJ : 22 The Poplars, Rockley Park, Napier Road, Poole, Dorset
            "10023691106",  # BH154LZ -> BH165BJ : 17 Pine Ridge, Rockley Park, Napier Road, Poole, Dorset
            "10023691494",  # BH154LZ -> BH165BJ : 37 The Poplars, Rockley Park, Napier Road, Poole, Dorset
            "10023691204",  # BH154LZ -> BH165BJ : 42 Rockley Vale, Rockley Park, Napier Road, Poole, Dorset
            "10023691437",  # BH154LZ -> BH165BJ : 6 The Oaks, Rockley Park, Napier Road, Poole, Dorset
            "10023691477",  # BH154LZ -> BH165BJ : 20 The Poplars, Rockley Park, Napier Road, Poole, Dorset
            "10023691223",  # BH154LZ -> BH165BJ : 60 Rockley Vale, Rockley Park, Napier Road, Poole, Dorset
            "10023691329",  # BH154LZ -> BH165BJ : 99 Lytchett Bay View, Rockley Park, Napier Road, Poole, Dorset
            "10023691261",  # BH154LZ -> BH165BJ : 31 Lytchett Bay View, Rockley Park, Napier Road, Poole, Dorset
            "10023691221",  # BH154LZ -> BH165BJ : 59 Rockley Vale, Rockley Park, Napier Road, Poole, Dorset
            "10024153347",  # BH76AN -> BH76AR : The Coach House, 841 Christchurch Road, Bournemouth, Dorset
        ]:
            rec["accept_suggestion"] = False

        return rec
