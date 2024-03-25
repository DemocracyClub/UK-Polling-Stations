from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = "2024-05-02/2024-04-11T11:20:01.019608/DC POlling Districts.csv"
    stations_name = "2024-05-02/2024-04-11T11:20:01.019608/DC Polling Stations.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094250773",  # 5A CHAPEL LANE, THORRINGTON, COLCHESTER
        ]:
            return None
        if record.postcode in [
            "CO12 4QT",  # split
            # suspect
            "CO15 1HW",
            "CO15 3BN",
            "CO15 1JG",
            "CO15 1HN",
            "CO15 1JL",
        ]:
            return None
        return super().address_record_to_dict(record)
