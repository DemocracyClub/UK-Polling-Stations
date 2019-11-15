from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000004"
    addresses_name = "parl.2019-12-12/Version 1/stockton.gov.uk-1573042249000-.tsv"
    stations_name = "parl.2019-12-12/Version 1/stockton.gov.uk-1573042249000-.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # Probable new builds throwing centroid outside of LA warning.
        if record.post_code == "TS21 3FJ":
            return None

        if uprn in [
            "10013728465",  # TS225AS -> TS225ER : Flat The Whitehouse, Whitehouse Road, Billingham
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10009306411",  # TS160QH -> TS160QT : Orchard Grange, A67 Eaglescliffe, Eaglescliffe, Stockton-on-Tees
        ]:
            rec["accept_suggestion"] = False

        return rec
