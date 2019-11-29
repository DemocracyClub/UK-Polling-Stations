from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000020"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019telford.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019telford.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "TF10 8AB":
            return None

        if uprn in [
            "452071472",  # TF43JZ -> TF43JX : The White Horse, Finger Road, Dawley, Telford, Shropshire
            "452041200",  # TF109HN -> TF109HW : Abbotts Way, Abbey Road, Lilleshall, Newport, Shropshire
            "10091738061",  # TF107HD -> TF107HF : Ground Floor Flat, 48 Wellington Road, Newport, Shropshire
            "10091738062",  # TF107HD -> TF107HF : First Floor Flat, 48 Wellington Road, Newport, Shropshire
            "452063592",  # SY44RF -> SY44RQ : Rose Cottage, Somerwood, Rodington, Shrewsbury, Shropshire
            "10024238558",  # TF26DN -> TF26DW : Flat Dominos Pizza, Holyhead Road, Oakengates, Telford, Shropshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200000670794",  # TF16RB -> TF15GH : 27A Castle Houses, Castle Street, Hadley, Telford, Shropshire
            "10024238030",  # TF87BJ -> TF87DN : Annexe At Greenacres, Buildwas Road, Ironbridge, Telford, Shropshire
        ]:
            rec["accept_suggestion"] = False

        return rec
