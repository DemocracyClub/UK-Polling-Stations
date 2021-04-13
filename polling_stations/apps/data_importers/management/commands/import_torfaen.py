from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TOF"
    addresses_name = (
        "2021-03-15T11:44:05.081204/Torfaen polling_station_export-2021-03-15.csv"
    )
    stations_name = (
        "2021-03-15T11:44:05.081204/Torfaen polling_station_export-2021-03-15.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013477024",  # AWEL MYNYDD, MANOR ROAD, ABERSYCHAN, PONTYPOOL
            "200002953610",  # YNYS NEWYDD, VALENTINE ROAD, COED YR EOS, ABERSYCHAN, PONTYPOOL
            "200002953605",  # TY COED YR EOS, VALENTINE ROAD, COED YR EOS, ABERSYCHAN, PONTYPOOL
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
            "10013477141",  # GELLI FAWR FARM, HENLLYS, CWMBRAN
            "10013478138",  # PENWYRLOD FARM PEN Y WYRLOD FARM ACCESS, HENLLYS, CWMBRAN
        ]:
            return None

        if record.housepostcode in [
            "NP4 7NW",
            "NP4 8LG",
            "NP44 1LE",
            "NP44 4QS",
            "NP4 6TX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # FORGESIDE COMMUNITY CENTRE FORGESIDE COMMUNITY CENTRE BFORGESIDE BLAENAVON TORFAEN NP4 9BD
        if record.pollingstationname == "FORGESIDE COMMUNITY CENTRE":
            record = record._replace(pollingstationpostcode="NP4 9DH")

        # ST MARYS CHURCH HALL BRYN EGLWYS CROESYCEILIOG CWMBRAN TORFAEN NP44  2E - changes two stations with same address
        if record.pollingstationname == "ST MARYS CHURCH HALL":
            record = record._replace(pollingstationpostcode="NP44 2EJ")

        # THORNHILL4UTOO THORNHILL COMMUNITY CENTRE LEADON COURT THORNHILL CWMBRAN TORFAEN NP44 5YZ
        if record.pollingstationname == "THORNHILL4UTOO":
            record = record._replace(pollingstationpostcode="NP44 5TZ")

        # GLASLYN COMMUNITY CENTRE GLASLYN COURT CROESYCEILIOG CWMBRAN TORFAEN - station change
        if record.pollingstationname == "GLASLYN COMMUNITY CENTRE":
            record = record._replace(
                pollingstationname="WOODLAND ROAD SOCIAL CENTRE",
                pollingstationaddress_1="CWMBRAN",
                pollingstationaddress_2="TORFAEN",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationpostcode="NP44 2DZ",
            )

        return super().station_record_to_dict(record)
