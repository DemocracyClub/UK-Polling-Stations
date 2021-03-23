from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HPL"
    addresses_name = "2021-03-19T11:33:42.492624/Polling Station Post code Finder.csv"
    stations_name = "2021-03-19T11:33:42.492624/Polling Station Post code Finder.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100110673527",  # THE CARAVAN X-PDI UNIT MIDDLETON ROAD, HARTLEPOOL
            "10090069600",  # MARSH HOUSE FARM, MARSH HOUSE LANE, GREATHAM, HARTLEPOOL
            "10090070990",  # 319 RABY ROAD, HARTLEPOOL
            "100110020815",  # 2 PHILLIPS ROAD, HARTLEPOOL
            "100110020667",  # ANELVILLE, THROSTON GRANGE LANE, HARTLEPOOL
            "10009716016",  # 4 MILBANK ROAD, HARTLEPOOL
            "10090072927",  # 76 MIDDLETON ROAD, HARTLEPOOL
            "10090072925",  # 2D BRAEMAR ROAD, HARTLEPOOL
            "10090072926",  # 2C BRAEMAR ROAD, HARTLEPOOL
            "100110673984",  # 2B BRAEMAR ROAD, HARTLEPOOL
            "10090073016",  # 2E BRAEMAR ROAD, HARTLEPOOL
            "100110009750",  # 49 EASINGTON ROAD, HARTLEPOOL
            "10095351223",  # 124A STOCKTON ROAD, HARTLEPOOL
            "10090072134",  # 105A STOCKTON ROAD, HARTLEPOOL
        ]:
            return None

        if record.addressline6 in [
            "TS24 9LL",
            "TS24 8DD",
            "TS25 5DY",
            "TS24 9BD",
            "TS25 5QB",
            "TS24 8PR",
            "TS25 5BF",
            "TS24 9SF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Hart Village Hall Front Street Hartlepool TS27 3A
        if record.polling_place_id == "10288":
            record = record._replace(polling_place_postcode="TS27 3AW")

        # Lynnfield Community & Learning Centre Creche Area - access through garden Elcho Street Hartlepool TS248HP
        if record.polling_place_id == "10408":
            record = record._replace(polling_place_postcode="TS26 8HP")

        # Browning Avenue Baptist Church Browning Avenue TS35 5PS
        if record.polling_place_id == "10335":
            record = record._replace(polling_place_postcode="TS25 5PS")

        # Owton Manor Baptist Church Catcote Road Hartlepool TS25 4RB
        if record.polling_place_id == "10355":
            record = record._replace(polling_place_postcode="TS25 3EF")

        return super().station_record_to_dict(record)
