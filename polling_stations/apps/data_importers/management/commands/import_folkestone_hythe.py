from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2024-07-04/2024-06-06T14:13:30.378574/SHE_PD_combined.tsv"
    stations_name = "2024-07-04/2024-06-06T14:13:30.378574/SHE_PS_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "50128588",  # RESIDENTIAL UNIT 1 57 DOVER ROAD, FOLKESTONE
        ]:
            return None

        if record.postcode in [
            # split
            "TN29 9AU",
            "TN28 8PW",
            "CT20 3RE",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Amendment from council:
        # Moves point closer to access road, corrects postcode:
        # Hawkinge Pavilion and Sports Ground, Pavilion Road, Hawkinge, Kent, CT18 7UA
        if record.stationcode == "128":
            record = record._replace(
                xordinate="621844",
                yordinate="140818",
                postcode="CT18 7UA",
            )
        return super().station_record_to_dict(record)
