from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2024-07-04/2024-05-28T15:07:15.444005/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T15:07:15.444005/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Change of station
        # Old: Northgate Community Centre, Barnfield Road, RH10 8DS
        # New: St. Elizabeth’s Church, RH10 8DS
        if record.polling_place_id == "1579":
            record = record._replace(
                polling_place_name="St. Elizabeth’s Church",
                polling_place_address_1="(formally Louise Ryrie Dance School)",
                polling_place_address_2="corner of Barnfield Road and Boundary Road,",
                polling_place_address_3="Northgate",
                polling_place_address_4="Crawley",
                polling_place_postcode="RH10 8DS",
                polling_place_easting="527314",
                polling_place_northing="137286",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061788135",  # 79 PUNCH COPSE ROAD, CRAWLEY
            "100061767151",  # OAK COTTAGE, BALCOMBE ROAD, CRAWLEY
            "200001244362",  # PREMIER INN, CRAWLEY AVENUE, CRAWLEY
        ]:
            return None

        return super().address_record_to_dict(record)
