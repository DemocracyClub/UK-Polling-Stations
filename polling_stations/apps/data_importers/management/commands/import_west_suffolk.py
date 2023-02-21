from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WSK"
    addresses_name = "2021-03-19T13:58:06.894064/Democracy Club 6 May 2021.CSV"
    stations_name = "2021-03-19T13:58:06.894064/Democracy Club 6 May 2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090002658",  # 164 LONDON ROAD, BRANDON
            "10001258706",  # 129 HIGH STREET, LAKENHEATH, BRANDON
            "10001258707",  # 129A HIGH STREET, LAKENHEATH, BRANDON
            "10001255117",  # 131 HIGH STREET, LAKENHEATH, BRANDON
            "10090737493",  # 152 WESTLEY ROAD, BURY ST EDMUNDS
            "100091029230",  # 23 BURY ROAD, NEWMARKET
            "200001370253",  # 27 BURY ROAD, NEWMARKET
            "10094770713",  # THE ANNEXE ATTLETON FARM ATTLETON GREEN, WICKHAMBROOK
            "10001255061",  # DELPH COTTAGE DELPH DROVE, WEST ROW
            "10023126363",  # HEAVEN, THETFORD ROAD, CONEY WESTON, BURY ST. EDMUNDS
        ]:
            return None

        if record.addressline6 in ["CB8 9AW", "CB9 7NL", "CB8 8JH"]:
            return None

        if "Room" in record.addressline1 and "1 The Avenue" == record.addressline2:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Lakenheath Peace Memorial Hall, High Street, Lakenheath, Suffolk, IP27 9WE
        if record.polling_place_id == "15966":
            record = record._replace(
                polling_place_name="Lakenheath Community Centre",
                polling_place_address_2="Lakenheath",
                polling_place_address_3="Suffolk",
                polling_place_address_4="",
                polling_place_postcode="IP27 9DS",
            )

        return super().station_record_to_dict(record)
