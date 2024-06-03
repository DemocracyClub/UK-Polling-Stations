from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = "2024-07-04/2024-06-04T09:01:23.444439/CHL_combined.tsv"
    stations_name = "2024-07-04/2024-06-04T09:01:23.444439/CHL_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    ## Ignoring the warnings RE the following stations
    ## (Council has confirmed the current postcodes are correct):
    ## 'East Hanningfield Village Hall, The Tye, East Hanningfield, Chelmsford, CM3 8AE' (id: 13209)
    ## 'Civic Centre - Chelmsford City Council, Duke Street, Chelmsford, CM1 1JE' (id: 13420)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091430409",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMSFORD
            "10093928503",  # 67 BROOMFIELD ROAD, CHELMSFORD
            "200004630041",  # 1 LIBERTY WAY, RUNWELL, WICKFORD
            "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD
            "200004627211",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMSFORD
            "10093928515",  # CARAVAN 2 AT OAKVALE DOMSEY LANE, LITTLE WALTHAM, CHELMSFORD
        ]:
            return None

        if record.addressline6 in [
            # split
            "CM1 7AR",
            "CM1 1FU",
            "CM3 1ER",
            "CM4 9JL",
        ]:
            return None

        return super().address_record_to_dict(record)
