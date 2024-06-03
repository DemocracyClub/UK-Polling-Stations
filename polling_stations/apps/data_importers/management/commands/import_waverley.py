from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WAE"
    addresses_name = "2024-07-04/2024-06-11T16:14:05.131641/WAE_combined.tsv"
    stations_name = "2024-07-04/2024-06-11T16:14:05.131641/WAE_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100061602142",  # 3 FARNBOROUGH ROAD, FARNHAM
            "100062350984",  # 25 HIGH STREET, CRANLEIGH
            "200002335818",  # WHITE PLACE, 19 HIGH STREET, CRANLEIGH
            "100062339000",  # EASEDALE, WHITMORE VALE ROAD, HINDHEAD
            "200001293824",  # TRUXFORD STREAM THURSLEY ROAD, ELSTEAD, GODALMING
            "100061618397",  # HANDON COTTAGE, MARKWICK LANE, LOXHILL, GODALMING
            "100061618401",  # SHENTONS COTTAGE, MARKWICK LANE, LOXHILL, GODALMING
        ]:
            return None

        if record.postcode in [
            # splits
            "GU9 0NZ",
            "GU9 9JT",
            # looks wrong
            "RH12 3BQ",
            "GU6 8EJ",
        ]:
            return None

        return super().address_record_to_dict(record)
