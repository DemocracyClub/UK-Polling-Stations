from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LBH"
    addresses_name = (
        "2024-05-02/2024-03-06T17:57:26.808182/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-06T17:57:26.808182/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021858462",  # 10 BELVEDERE COURT KINGS AVENUE, LONDON
            "100021858466",  # 14 BELVEDERE COURT KINGS AVENUE, LONDON
            "10008788781",  # LODGE NORWOOD CEMETERY NORWOOD HIGH STREET, LONDON
            "100021860715",  # 2 LAMBERHURST ROAD, LONDON
            "100021868483",  # 130 LYHAM ROAD, LONDON
            "200000477497",  # 1 PABLO NERUDA CLOSE, LONDON
            "200000477498",  # 2 PABLO NERUDA CLOSE, LONDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SW2 5RS",
            "SW8 2EN",
            "SE11 5UG",
            "SE21 8HX",
            "SW16 2UU",
            "SW9 6ED",
            "SW9 9NT",
            "SW9 7AR",
            "SW9 6HN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add point for: Weir Link Community Centre, 33 Weir Road, London, SW12 0NU
        if record.polling_place_id == "7494":
            record = record._replace(polling_place_easting="529369")
            record = record._replace(polling_place_northing="173631")

        # add point for: Elmgreen Secondary School, Elmcourt Road, London, SE27 9BZ
        if record.polling_place_id == "7402":
            record = record._replace(polling_place_easting="532013")
            record = record._replace(polling_place_northing="172802")

        return super().station_record_to_dict(record)
