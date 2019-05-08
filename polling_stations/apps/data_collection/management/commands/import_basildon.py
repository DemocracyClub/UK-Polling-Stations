from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000066"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 basildon.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 basildon.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # station changes for EU election
        if record.polling_place_id == "3968":
            record = record._replace(
                polling_place_name="Portacabin at Brightside County Primary School"
            )
        if record.polling_place_id == "4095":
            record = record._replace(
                polling_place_name="Portacabin at Ryedene Primary & Nursery School"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        ### Invalid postcodes

        # 62A Brightside, Billericay, Essex
        if uprn == "10093028037":
            rec["postcode"] = "CM120LE"
        # 7 Tate House, Tate Close, Basildon, Essex
        if uprn == "10093026159":
            rec["postcode"] = "SS155BE"
        # 21 The Nave, Laindon, Basildon, Essex
        if uprn == "10013353584":
            rec["postcode"] = "SS155NW"
        # Ella, Cromer Avenue, Laindon, Basildon, Essex
        if uprn == "10093029352":
            rec["postcode"] = "SS15 6HU"
        # Hotel Room at Tyrrell Court, Tyrrell Court, Crest Avenue, Pitsea, Basildon, Essex
        if uprn == "10093028660":
            rec["postcode"] = "SS13 2EE"

        ### Postcode mismatches
        if uprn in [
            "100091432735",  # CM129BY -> CM129BE : Flat 1a King George Court (1st Floor), High Street, Billericay, Essex
            "100091212721",  # CM129SS -> CM129PX : The Burstead Golf Club, Tye Common Road, Little Burstead, Billericay, Essex
            "10024196288",  # SS156GJ -> SS156GH : 15 School Avenue, Laindon, Basildon, Essex
            "10024197480",  # SS156GH -> SS156GJ : 44 School Avenue, Laindon, Basildon, Essex
            "10024197481",  # SS156GH -> SS156GJ : 46 School Avenue, Laindon, Basildon, Essex
            "10093026829",  # SS156GJ -> SS156LX : 144 School Avenue, Laindon, Basildon, Essex
            "100090277964",  # CM120ND -> CM120NH : 111 Perry Street, Billericay, Essex
            "10093029314",  # SS165LE -> SS155LE : 7 Bebington Link, Basildon, Essex
            "10093029315",  # SS165LE -> SS155LE : 8 Bebington Link, Basildon, Essex
            "10093029317",  # SS165LE -> SS155LE : 10 Bebington Link, Basildon, Essex
            "10024197241",  # SS156PF -> SS156PE : 29 Somerset Road, Laindon, Basildon, Essex
            "100090233401",  # SS133EA -> SS132EA : 17 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233418",  # SS132EB -> SS132EA : 34 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233419",  # SS132EB -> SS132EA : 35 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233422",  # SS132EB -> SS132EA : 38 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233423",  # SS132EB -> SS132EA : 39 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233424",  # SS132EB -> SS132EA : 40 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233425",  # SS132EB -> SS132EA : 41 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100090233427",  # SS132EB -> SS132EA : 43 Appleford Court, Halstow Way, Pitsea, Basildon, Essex
            "100091210125",  # SS132LG -> SS132DJ : Willow Cottage, Eversley Road, Pitsea, Basildon, Essex
            "10013353242",  # SS155UN -> SS155NP : 82 Laindon Link, Laindon, Basildon, Essex
            "10024197236",  # SS155UN -> SS155NP : 80 Laindon Link, Laindon, Basildon, Essex
            "200001621243",  # SS155UN -> SS155NP : 92 Laindon Link, Laindon, Basildon, Essex
            "200001621241",  # SS155UN -> SS155NP : 86 Laindon Link, Laindon, Basildon, Essex
            "100090260223",  # SS132EA -> SS133EA : 30 Rokescroft, Pitsea, Basildon, Essex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10093029374",  # CM112AD -> CM120AD : 2 Woodward House, 9 Stock Road, Billericay, Essex
            "10024196317",  # CM129LH -> SS156GH : 45 School Road, Billericay, Essex
            "10090681494",  # CM129JD -> CM111EX : 179A Western Road, Billericay, Essex
            "100090284447",  # SS129EJ -> SS120EG : Mobile Home Adj. Cranfield, Lower Park Road, Wickford, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
