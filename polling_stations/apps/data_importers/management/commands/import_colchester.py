from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = "2021-04-09T11:23:24.223959/Polling Stations - Colchester.tsv"
    stations_name = "2021-04-09T11:23:24.223959/Polling Stations - Colchester.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "10697",  # Queen Elizabeth Hall Annexe, New Cut, Layer-de-la-Haye, Colchester CO2 0EH
            "10798",  # Old Heath Community Centre, D'Arcy Road, Old Heath, Colchester CO2 8BB
            "10738",  # Abberton & Langenhoe Village Hall, Edward Marke Drive, Langenhoe, Colchester CO5 7LP
            "10801",  # Rowhedge Village Hall, Rectory Road, Rowhedge, Colchester CO5 7HX
            "10985",  # Theatricool Studio, Belle Vue Road, Colchester CO1 1XA
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091238419",  # LAUREL COTTAGE, BIRCH STREET, BIRCH, COLCHESTER
            "10093741451",  # 82 MALDON ROAD, TIPTREE, COLCHESTER
            "10093741447",  # 84A MALDON ROAD, TIPTREE, COLCHESTER
            "303008568",  # MAIN NURSES HOME ESSEX COUNTY HOSPITAL LEXDEN ROAD, COLCHESTER
            "10070237642",  # HOME FARM BUNGALOW A133 WESTBOUND, COLCHESTER
            "10004962495",  # 1 COLLIERS FARM COTTAGES, ELMSTEAD ROAD, COLCHESTER
            "10004967099",  # 2 COLLIERS FARM COTTAGES, ELMSTEAD ROAD, COLCHESTER
            "10095443897",  # RUNKINS FARM LANGHAM LANE, BOXTED
            "10034897285",  # CARAVAN 2 BRIDGESIDE TURKEY COCK LANE, STANWAY
            "10091123105",  # B-3-04-B BIRCH HAVEN ROAD, COLCHESTER
        ]:
            return None

        if record.addressline6 in [
            "CO3 3TW",
            "CO2 9JX",
            "CO2 8BU",
            "CO3 8LX",
            "CO5 7DB",
            "CO3 3DA",
            "CO5 0PU",
            "CO4 5LG",
            "CO7 9LE",
            "CO7 9FN",
        ]:
            return None

        return super().address_record_to_dict(record)
