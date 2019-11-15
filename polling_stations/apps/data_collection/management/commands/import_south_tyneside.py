from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000023"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019s tynes.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019s tynes.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        if (
            record.addressline1.endswith(" Long Row")
            and record.addressline6 == "NE31 1JA"
        ):
            record = record._replace(addressline6="NE33 1JA")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100000345804":
            return None

        if uprn in [
            "200000002007"  # NE340PW -> NE340YE : Staff Residence, 169 Harton Lane, South Shields
        ]:
            rec["accept_suggestion"] = True

        return rec
