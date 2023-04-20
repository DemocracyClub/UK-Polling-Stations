from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PTE"
    addresses_name = (
        "2023-05-04/2023-04-17T09:51:32.818127/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T09:51:32.818127/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094542529",  # 64 GREENFIELD WAY, HAMPTON WATER, PETERBOROUGH
            "10090763503",  # MEDICAL & STAFF ACCOMMODATION BLOCK, PETERBOROUGH CITY HOSPITAL, BRETTON GATE, BRETTON, PETERBOROUGH
            "100091206701",  # WOODLANDS, HAM LANE, ORTON WATERVILLE, PETERBOROUGH
            "10008073540",  # 1 NEWARK AVENUE, PETERBOROUGH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PE7 0LE",
            "PE3 8AA",  # KATHARINE WAY, BRETTON, PETERBOROUGH
            "PE7 8RU",  # WILTON AVENUE, HAMPTON GARDENS, PETERBOROUGH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Copeland Community Centre, 37 Copeland, Bretton, Peterborough, PE3 9YJ
        # Proposed correction: PE3 6YJ
        if record.polling_place_id == "9666":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
