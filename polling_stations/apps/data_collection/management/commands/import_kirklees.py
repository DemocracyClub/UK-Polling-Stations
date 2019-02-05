from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000034"
    addresses_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "83099017":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "BD19 5EY"
            return rec

        if uprn == "200003798939":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "HD7 5TU"
            return rec

        if uprn == "83242159":
            return None

        if uprn == "83246005":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "HD2 1HA"
            return rec

        return super().address_record_to_dict(record)
