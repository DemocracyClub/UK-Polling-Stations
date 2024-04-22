from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PTE"
    addresses_name = (
        "2024-05-02/2024-04-12T13:00:19.878088/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T13:00:19.878088/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094542529",  # 64 GREENFIELD WAY, HAMPTON WATER, PETERBOROUGH
            "100091206701",  # WOODLANDS, HAM LANE, ORTON WATERVILLE, PETERBOROUGH
            "100090190220",  # 296 EASTFIELD ROAD, PETERBOROUGH
            "100091511753",  # 294 EASTFIELD ROAD, PETERBOROUGH
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "PE3 8AA",
            "PE1 4RZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Copeland Community Centre, 37 Copeland, Bretton, Peterborough, PE3 9YJ
        if record.polling_place_id == "10083":
            record = record._replace(polling_place_postcode="PE3 6YJ")

        return super().station_record_to_dict(record)
