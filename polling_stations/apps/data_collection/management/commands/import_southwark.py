from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000028"
    addresses_name = (
        "2020-02-17T14:30:02.399947/EC & Democracy Club Polling Place Look Up 2020.csv"
    )
    stations_name = (
        "2020-02-17T14:30:02.399947/EC & Democracy Club Polling Place Look Up 2020.csv"
    )
    elections = ["2020-05-07"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline2 == "179 Forest Hill Road":
            return None

        if record.addressline1 == "Excluding Third Floor and Fourth Floor":
            return None

        if record.addressline6 in [
            "SE16 2EZ",
            "SE21 7BG",
            "SE1 0AA",
            "SE1 0NS",
            "SE15 4TP",
        ]:
            return None

        if uprn in [
            "10094086807",
            "200003480357",
            "10093341595",
            "10093341594",
            "10093341119",
            "10090283768",
            "10094086939",
            "10090747304",
            "10093340214",
            "10009806727",
            "200003492155",
            "10090748785",
        ]:
            return None

        if uprn == "200003487670":
            rec["postcode"] = "SE1 2BB"

        if uprn == "10091665680":
            rec["uprn"] = ""
            rec["postcode"] = "SE5 0EZ"

        if uprn == "10093340235":
            rec["postcode"] = "SE22 9EE"

        return rec
