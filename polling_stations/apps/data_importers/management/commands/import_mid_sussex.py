from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2021-03-26T11:11:22.528819/Democracy_Club__06May2021 Mid Sussex.tsv"
    )
    stations_name = (
        "2021-03-26T11:11:22.528819/Democracy_Club__06May2021 Mid Sussex.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Church Hall, St Edward the Confessor Church
        if record.polling_place_id == "3445":
            rec["location"] = Point(-0.14863, 50.96048, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093413710",  # 13 THE HOLT, HAYWARDS HEATH
            "10070621745",  # 149 ROYAL GEORGE ROAD, BURGESS HILL
        ]:
            return None

        if record.post_code in [
            "RH19 2DL",
            "RH10 4SH",
            "RH19 4LF",
            "RH16 2QG",
            "RH16 2QB",
            "RH16 2QF",
            "RH17 5AL",
            "RH17 5UQ",
            "RH15 8AZ",
            "RH15 9QU",
            "BN6 9NE",
            "RH16 4ET",
            "RH19 1ET",
        ]:
            return None

        return super().address_record_to_dict(record)
