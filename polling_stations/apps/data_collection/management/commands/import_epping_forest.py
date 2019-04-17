from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000072"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019epping.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019epping.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "2497":
            record = record._replace(polling_place_easting="551593")
            record = record._replace(polling_place_northing="211197")

        if record.polling_place_id == "2509":
            record = record._replace(polling_place_easting="538647")
            record = record._replace(polling_place_northing="196512")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012155997"  # CM195DA -> CM195DB : Keeper's Cottage, Epping Road, Roydon, Harlow
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10093181267",  # EN92HF -> CM166HF : 1 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181268",  # EN92HF -> CM166JE : 2 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181269",  # EN92HF -> CM166JE : 3 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181270",  # EN92HF -> CM166JE : 4 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181271",  # EN92HF -> CM166JE : 5 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181272",  # EN92HF -> CM166JE : 6 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181273",  # EN92HF -> CM166JE : 7 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181274",  # EN92HF -> CM166JE : 8 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10093181275",  # EN92HF -> CM166JE : 9 Elizabeth Close, Nazeing Road, Nazeing, Waltham Abbey
            "10012157506",  # CM165HS -> CM165HH : The Dairy, Copped Hall, Epping
            "10012157524",  # CM165HS -> CM165HH : Link House, Copped Hall, Epping
            "100091437000",  # CM165HS -> CM165HR : London Lodge West, Copped Hall (E), Epping
            "100091437005",  # CM165HS -> CM165HR : London Lodge East, Crown Hill (E), Epping
            "10012154745",  # CM59LA -> CM59LD : The Old Rectory, Greensted Road, Ongar
            "10012160996",  # EN92SF -> EN92DF : Farm House, Harold Park Farm, Nazeing, Waltham Abbey
            "10013930559",  # CM179NG -> CM170RE : The Flat at The Gatekeeper, London Road, Harlow
        ]:
            rec["accept_suggestion"] = False

        return rec
