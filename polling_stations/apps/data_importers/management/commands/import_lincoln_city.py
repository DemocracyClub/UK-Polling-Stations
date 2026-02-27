from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "LIC"
    addresses_name = "2026-05-07/2026-02-27T10:25:51.258710/Democracy Club - Idox_2026-02-27 10-24.csv"
    stations_name = "2026-05-07/2026-02-27T10:25:51.258710/Democracy Club - Idox_2026-02-27 10-24.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "235039692",  # 23 DEVON STREET, LINCOLN, LN2 5NT
            "235056965",  # FLAT CROWN AND ARROWS MOORLAND AVENUE, LINCOLN
        ]:
            return None

        if record.postcode in [
            # split
            "LN6 0LH",
            "LN2 4RP",
            "LN1 1BU",
            "LN1 1QD",
            "LN5 8AG",
            "LN6 8AZ",
            "LN2 4DY",
            "LN1 1PH",
            "LN5 7LA",
            "LN2 4NA",
            "LN6 8DB",
            "LN2 5EJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Missing point for: Portacabin Nettleham Road Shopping Centre Entrance from Wolsey Way Nettleham Road Lincoln
        # Ignore: Address is correct and there is no postcode on https://www.nelincs.gov.uk/

        # removes wrong UPRN for: St Peter in Eastgate Church, Eastgate, Lincoln, LN2 4AA
        if self.get_station_hash(record) == "45-st-peter-in-eastgate-church":
            record = record._replace(pollingvenueuprn="")

        return super().station_record_to_dict(record)
