from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000180"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy Club Data Vale of White Horse.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy Club Data Vale of White Horse.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Polling place grid ref wrong.
        if record.polling_place_id in ["6822"]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # postcodes with implausible pollingstations.
        if uprn in [
            "10093199584",
            "10093199586",
            "10094276967",
            "10093199585",
            "10093199588",
            "10094276965",
            "10094276964",
            "10093199587",
            "10094276966",
            "10094276968",
        ]:
            return None

        if uprn in [
            "10093195669"  # OX29AH -> OX29PH : 136, Apt 2, Cumnor Hill, Cumnor, Oxford, Oxfordshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10093196551"  # OX116GE -> OX110ED : 5 Mezereon Spur, Mezereon Spur, Harwell, Didcot
        ]:
            rec["accept_suggestion"] = False

        # Addressbase georeferencing incorrect
        if uprn in [
            "10093196937",
            "10093196928",
            "10093196926",
            "10093196931",
            "10093196930",
            "10093196929",
            "10093196936",
            "10093196940",
            "10093196939",
            "10093196933",
            "10093196925",
            "10093196941",
            "10093196935",
            "10093196932",
            "10093196938",
            "10093196927",
            "10093196934",
        ]:
            rec["accept_suggestion"] = False

        return rec
