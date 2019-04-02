from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000010"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Hull.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Hull.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        address = record.addressline1
        if "Marl Park" in address:
            rec["polling_station_id"] = "9663"

        if "Larkin Lane" in address:
            rec["polling_station_id"] = "9610"

        if "Joe Tasker Way" in address:
            rec["polling_station_id"] = "9684"

        if uprn in [
            "21111021",  # HU52QS -> HU52RA : 44A Princes Road, Kingston Upon Hull
            "21124359",  # HU53LT -> HU53LR : 110 Belvoir Street, Kingston upon Hull
            "21062783",  # HU53JT -> HU53JX : 110 Marlborough Avenue, Kingston upon Hull
            "21075981",  # HU53QG -> HU53QA : The Bowery, 32 Princes Avenue, Kingston upon Hull
            "21109523",  # HU53QG -> HU53QA : 28A Princes Avenue, Kingston upon Hull
            "21110995",  # HU53QG -> HU53QA : Flat, 14 Princes Avenue, Kingston upon Hull
            "21109524",  # HU53QG -> HU53QA : 28B Princes Avenue, Kingston upon Hull
            "10024009551",  # HU53QG -> HU53QA : Flat Above Pave, 16/20 Princes Avenue, Kingston upon Hull
            "21129686",  # HU52NN -> HU53AA : (Flat), 110 Newland Avenue, Kingston upon Hull
            "21110796",  # HU55NT -> HU55PB : 18A Manor Road, Kingston Upon Hull
            "21109590",  # HU93AB -> HU93HA : (Flat), 22 Southcoates Lane, Kingston Upon Hull
            "21109042",  # HU89DA -> HU89AN : Flat, 869 Holderness Road, Kingston upon Hull
            "21004585",  # HU94HL -> HU94HN : 4 Amethyst Road, Kingston Upon Hull
            "21004583",  # HU94HL -> HU94HN : 2 Amethyst Road, Kingston Upon Hull
            "21109870",  # HU94HL -> HU94HN : 1A Amethyst Road, Kingston Upon Hull
            "21004584",  # HU94HN -> HU94HL : 3 Amethyst Road, Kingston upon Hull
            "21004586",  # HU94HN -> HU94HL : 5 Amethyst Road, Kingston upon Hull
            "21004589",  # HU94HN -> HU94HL : 11 Amethyst Road, Kingston upon Hull
            "21004590",  # HU94HN -> HU94HL : 13 Amethyst Road, Kingston upon Hull
            "21110849",  # HU92NX -> HU92NU : 168A New Bridge Road, Kingston Upon Hull
            "10024645653",  # HU93UA -> HU93TR : Alexandra Court Care Centre, 340 Southcoates Lane, Kingston Upon Hull
            "21123706",  # HU36AB -> HU33PB : West Park Nursing Home, 1-5 Selby Street, Kingston Upon Hull
            "1000863966",  # HU11RS -> HU11RQ : King William Hotel, 41 Market Place, Kingston Upon Hull
            "10093951676",  # HU88LG -> HU88LQ : 273A James Reckitt Avenue, Kingston Upon Hull
        ]:
            rec["accept_suggestion"] = True

            if uprn in [
                "21088100"  # HU88TH -> HU95SR : 119 Severn Street, Kingston Upon Hull
            ]:
                rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        # Balfour Street Community Centre Balfour Street/Victor Street
        if record.polling_place_id == "9582":
            record = record._replace(polling_place_postcode="HU9 2EU")
        # Mitchell Community Centre Goodrich Close Fountain Road
        if record.polling_place_id == "9554":
            record = record._replace(polling_place_postcode="HU2 0BQ")
        # Mobile Unit Wansbeck Primary School Playing Fields Wansbeck Road (Near Tamar Grove) Hull
        if record.polling_place_id == "9628":
            record = record._replace(polling_place_postcode="HU8 9SR")

        return super().station_record_to_dict(record)
