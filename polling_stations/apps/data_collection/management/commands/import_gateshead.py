from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000037"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019gates.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019gates.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100000084114",  # NE404NG -> NE404NB : Allendale House, Garden Terrace, Crawcrook, Ryton
            "100000083763",  # NE403HF -> NE403RS : Orchard House, Lane Head, Ryton
            "10024187613",  # NE95XP -> NE95XB : Spion Kop North, Primrose Hill, Sheriff Hill, Gateshead
            "10024187614",  # NE95XP -> NE95XB : Landscape Cottage, Primrose Hill, Sheriff Hill, Gateshead
            "100000057892",  # NE108UJ -> NE404FA : 3 Stanton Close, Wardley, Gateshead
            "100000057890",  # NE108UJ -> NE404FA : 1 Stanton Close, Wardley, Gateshead
            "100000057894",  # NE108UJ -> NE404FA : 5 Stanton Close, Wardley, Gateshead
            "100000057900",  # NE108UJ -> NE404FA : 11 Stanton Close, Wardley, Gateshead
            "100000057896",  # NE108UJ -> NE404FA : 7 Stanton Close, Wardley, Gateshead
            "100000057891",  # NE108UJ -> NE404FA : 2 Stanton Close, Wardley, Gateshead
            "100000086887",  # NE403PG -> NE403PL : Tower Lodge, Whitewell Lane, Ryton
        ]:
            rec["accept_suggestion"] = False

        return rec
