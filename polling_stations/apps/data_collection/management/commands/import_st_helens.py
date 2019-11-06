from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000013"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sthel.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019sthel.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "3607":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        if record.polling_place_id == "3670":
            record = record._replace(polling_place_easting="350436")
            record = record._replace(polling_place_northing="394900")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "39086246":
            return None

        # UPRNs 39089002 through 39089022 look fishy. Not sure if it's council or addressbase. PC: WA95GG
        if "Alexander Court" in record.addressline1:
            rec["uprn"] = ""
            rec["accept_suggestion"] = False

        if (
            uprn == "39091800"
        ):  # 79 Newlove Avenue, WA119TB. NB addressbase UPRN is "39091800"
            rec["postcode"] = "WA104DS"
        if (
            uprn == "39093918"
        ):  # 32 Cunningham Court, WA101JT. NB addressbase UPRN is "39091918"
            rec["postcode"] = "WA104GA"
        if uprn == "39099008":  # 22 Dorothy Street, WA92RL
            rec["postcode"] = "WA95RL"
        if uprn == "39097964":  # 107A Springfield Road, WA93RR
            rec["postcode"] = "WA103RR"
            rec["accept_suggestion"] = False

        if (
            uprn == "39094751"
        ):  # 14A Hartford Road, WA102TL. NB not obviously in Addressbase
            rec["postcode"] = "WA10 5QT"
        if (
            uprn == "39086545"
        ):  # 53 The Boulevard, WA102TJ. NB addressbase UPRN is "39096545"
            rec["postcode"] = "WA10 3UY"

        if uprn in [
            "39097186"  # WA93UF -> WA103UF : 17A Prescot Road, St Helens,, Merseyside",  # L354PZ -> L354PX : 1 The Orchard, Rainhill, Merseyside
        ]:
            rec["accept_suggestion"] = True

        return rec
