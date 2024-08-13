from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "AYL"
    addresses_name = "2021-03-18T17:32:05.640816/Bucks_dedupe.tsv"
    stations_name = "2021-03-18T17:32:05.640816/Bucks_dedupe.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "766039022",  # MANOR FARM, HILLESDEN ROAD, GAWCOTT, BUCKINGHAM
                "766258964",  # LOWER FARM, BERRYFIELDS GATED ROAD, QUARRENDON, AYLESBURY
                "10095501236",  # NARROWBOAT GENTLY BENTLEY, AYLESBURY BASIN, EXCHANGE STREET, AYLESBURY
                "10095500186",  # 35 YORK PLACE, AYLESBURY
                "766297815",  # THE WHITELEAF CENTRE, BIERTON ROAD, AYLESBURY
                "766259070",  # NB ODIN AYLESBURY BASIN EXCHANGE STREET, AYLESBURY
            ]
        ):
            return None

        if record.addressline6 in [
            "MK18 1PJ",
            "HP21 9HY",
            "MK17 0EW",
            "HP20 1UR",
            "MK18 3JZ",
        ]:
            return None

        return super().address_record_to_dict(record)
