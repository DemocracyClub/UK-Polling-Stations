from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAW"
    addresses_name = "2021-04-16T12:19:51.711968/Warwick Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-16T12:19:51.711968/Warwick Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071511663",  # CHELLOW DENE, KITES NEST LANE, BEAUSALE, WARWICK
            "100071258162",  # BUDBROOKE LODGE FARM, HAMPTON ROAD, WARWICK
            "100071258929",  # FLAT VINE INN 86-88 WEST STREET, WARWICK
            "100071257923",  # THE STUD COTTAGE, GUYS CLIFFE, WARWICK
            "100071257922",  # GUYS CLIFFE STABLES COVENTRY ROAD, GUYS CLIFFE, WARWICK
            "10013184069",  # THE BUNGALOW, GUYS CLIFFE STABLES, GUYS CLIFFE, WARWICK
            "100071258712",  # FLAT 32 SPINNEY HILL, WARWICK
            "10000211700",  # FLAT 1-2, 23 CLEMENS STREET, LEAMINGTON SPA
            "100071255338",  # 14B REGENCY HOUSE NEWBOLD TERRACE, LEAMINGTON SPA
            "10023406679",  # 44 WARWICK PLACE, LEAMINGTON SPA
            "10091560609",  # 8A DALEHOUSE LANE, KENILWORTH
            "10023407172",  # 18A REGENT STREET, LEAMINGTON SPA
            "100071250620",  # PETER R THOMPSON, STAGS HEAD FARM, BUBBENHALL ROAD, BAGINTON, COVENTRY
            "100070231043",  # FLAT 47, BEAUCHAMP COURT, BEAUCHAMP ROAD, KENILWORTH
            "10091559815",  # 20 SAYER CLOSE, LEAMINGTON SPA
        ]:
            return None

        if record.addressline6 in [
            "CV32 7BE",
            "CV32 6AN",
            "CV34 5BY",
            "CV32 7AW",
            "CV31 1BN",
            "CV8 2FE",
            "CV8 2GT",
            "CV32 5TA",
            "CV34 6RB",
            "CV32 5JG",
            "CV32 5EZ",
            "CV31 3PG",
            "CV34 8BN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Lapworth Village Hall (Main Hall) Old Warwick Road Lapworth B95 6LD
        if record.polling_place_id == "10734":
            record = record._replace(polling_place_postcode="")

        # Radford Semele Community Hall STATION B 68 Lewis Road Radford Semele CV31 1LQ
        # set to same as Radford Semele Community Hall STATION A 68 Lewis Road Radford Semele CV31 1UQ
        if record.polling_place_id == "10656":
            record = record._replace(polling_place_postcode="CV31 1UQ")

        return super().station_record_to_dict(record)
