from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2024-05-02/2024-03-06T09:57:53.761776/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-06T09:57:53.761776/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        ## Ignoring the warnings RE the following stations
        ## (Council has confirmed the current postcodes are correct):
        ## 'East Hanningfield Village Hall, The Tye, East Hanningfield, Chelmsford, CM3 8AE' (id: 13209)
        ## 'Civic Centre - Chelmsford City Council, Duke Street, Chelmsford, CM1 1JE' (id: 13420)

        # '11th Chelmsford Scout Group, Scout Hut, Gloucester Avenue, Chelmsford, CM2 9LG' (id: 13004)
        if record.polling_place_id == "13004":
            record = record._replace(polling_place_postcode="CM2 9DS")

        # 'Moulsham High Youth Centre, Access via path between 41 & 49 Gloucester Avenue, Chelmsford, CM2 9ES' (id: 13012)
        if record.polling_place_id == "13012":
            record = record._replace(polling_place_postcode="CM2 9DZ")

        # 'St Andrews Church, Melbourne Avenue, Chelmsford, CM1 2DT' (id: 13039)
        if record.polling_place_id == "13039":
            record = record._replace(polling_place_postcode="CM1 2JB")

        # 'St. John the Evangelist`s Church, Church Lane/Sandon Hill, Ford End, Chelmsford, Essex, CM3 1LQ' (id: 13103)
        if record.polling_place_id == "13103":
            record = record._replace(polling_place_postcode="CM3 1LH")

        # 'Pleshey Village Hall, The Street, Pleshey, Chelmsford, CM3 1HE' (id: 13131)
        if record.polling_place_id == "13131":
            record = record._replace(polling_place_postcode="CM3 1HB")

        # 'Our Lady Immaculate Church Hall, New London Road, Chelmsford, CM2 0AR' (id: 13147)
        if record.polling_place_id == "13147":
            record = record._replace(polling_place_postcode="CM2 0RG")

        # 'Rettendon Memorial Hall, Main Road, Rettendon, Chelmsford, CM3 8DP' (id: 13220)
        if record.polling_place_id == "13220":
            record = record._replace(polling_place_postcode="CM3 8DR")

        # 'Downham Village Hall, 50 School Road, Downham, Billericay, CM11 1QR' (id: 13231)
        if record.polling_place_id == "13231":
            record = record._replace(polling_place_postcode="CM11 1QP")

        return super().station_record_to_dict(record)

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
            "CM1 1FU",
            "CM1 7AR",
            "CM3 1ER",
            "CM4 9JL",
        ]:
            return None

        return super().address_record_to_dict(record)
