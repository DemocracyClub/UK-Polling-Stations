from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MTY"
    addresses_name = "2022-05-05/2022-03-25T08:16:11.219335/Eros_SQL_Output004.csv"
    stations_name = "2022-05-05/2022-03-25T08:16:11.219335/Eros_SQL_Output004.csv"
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "55":
            # PONTSTICILL MEMORIAL HALL, CF48 2UR
            # ignore 10034657547 Council says it's CF48 2UD
            record = record._replace(pollingstationpostcode="CF48 2UD")

        # Station Change from council
        # REAR OF THE WINDSOR HOTEL & BAR
        if record.pollingstationnumber == "37":
            record = record._replace(
                pollingstationname="MOBILE POLLING STATION",
                pollingstationaddress_1="BELLE VUE TERRACE",
                pollingstationaddress_2="MERTHYR VALE",
                pollingstationaddress_3="MERTHYR TYDFIL",
                pollingstationpostcode="CF48 4SP",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in ["10034658436"]:
            return None
        if record.housepostcode in [
            "CF48 1TL",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
