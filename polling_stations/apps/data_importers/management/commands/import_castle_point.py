from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = (
        "2022-05-05/2022-03-24T16:13:54.843482/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T16:13:54.843482/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100090361765",  # 35 LONDON ROAD, BENFLEET
            "100091600419",  # THE GRANGE, GRANGE ROAD, BENFLEET
            "10004934986",  # 5 STATION ROAD, CANVEY ISLAND
        ]:
            return None

        if record.addressline6 in [
            "SS8 8HN",
            "SS8 9SL",
        ]:
            return None

        return super().address_record_to_dict(record)
