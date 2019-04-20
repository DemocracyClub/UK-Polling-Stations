from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000032"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Brad.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Brad.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100051146371",  # BD62JZ -> BD62JY : Rock House, 200 Cemetery Road, Low Moor, Bradford
            "10010577818",  # BD133SW -> BD133SP : 34 Bottomley Holes, Thornton, Bradford
            "200004700106",  # BD128EW -> BD128EY : 1 Saxon Court, Wyke, Bradford
            "10010581458",  # BD205QN -> BD205QL : Riddlesden Golf Club House, 2 Howden Rough, Riddlesden, Keighley
            "100051272010",  # BD206PE -> BD206FQ : Longlands, Skipton Road, Steeton, Keighley
            "10024070042",  # BD48TJ -> BD48SY : Flat At, 2 Parry Lane, Bradford
            "100051122402",  # BD215RA -> BD215QU : Heather Lodge, Keighley Road, Hainworth Shaw, Keighley
            "200004702084",  # BD133SP -> BD133SW : 36 Cragg Lane, Thornton, Bradford
            "100051150769",  # BD133SP -> BD133SW : The Croft, Cragg Lane, Thornton, Bradford
        ]:
            rec["accept_suggestion"] = False

        if uprn == "10090402080":
            return None

        if record.addressline6 == "BD4 0BA":
            return None

        return rec
