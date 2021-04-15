from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MTY"
    addresses_name = (
        "2021-03-29T15:37:08.595129/Merthyr polling_station_export-2021-03-29.csv"
    )
    stations_name = (
        "2021-03-29T15:37:08.595129/Merthyr polling_station_export-2021-03-29.csv"
    )
    elections = ["2021-05-06"]
    csv_encoding = "latin-1"

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "42":
            # CWM GOLAU INTEGRATED CHILDREN'S CENTRE, DUFFRYN ROAD, PENTREBACH,
            # MERTHYR TYDFIL
            # "CF28 2DN" → "CF48 4BJ"
            # Source: UPRN 10034652721
            record = record._replace(pollingstationpostcode="CF48 4BJ")

        if record.pollingstationnumber == "60":
            # Trelewis OAP Hall, Bontnewydd Terrace, Trelewis
            # "CF48 6AG" → "CF46 6AF"
            # Address mentioned in an MP's newsletter; not in AddressBase
            # https://www.geraldjones.co.uk/wp-content/uploads/sites/256/2019/05/Gerald-Jones-Newsletter-April-2019.pdf
            record = record._replace(pollingstationpostcode="CF46 6AF")

        if record.pollingstationnumber == "25":
            # Georgetown Boys & Girls Club, Dynevor Street, Georgetown
            # "CF47 1AY" → "CF48 1AY"
            # https://find-and-update.company-information.service.gov.uk/company/08180489
            record = record._replace(pollingstationpostcode="CF48 1AY")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in ["CF48 3NE", "CF47 9AH", "CF48 1TL"]:
            return None  # split

        return super().address_record_to_dict(record)
