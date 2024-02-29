from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = "2024-05-02/2024-02-09T15:55:50.075896/Democracy_Club__02May2024_St Albans City and District Council.tsv"
    stations_name = "2024-05-02/2024-02-09T15:55:50.075896/Democracy_Club__02May2024_St Albans City and District Council.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Wood End School, Yeomans Avenue, Harpenden
        if record.polling_place_id == "5061":
            record = record._replace(polling_place_northing="215414")

        # coordinate correction from council:
        # Park Hall, Leyton Road, Harpenden, AL5 2LX
        if record.polling_place_id == "5084":
            record = record._replace(polling_place_northing="214003")
            record = record._replace(polling_place_easting="513471")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081131978",  # PADDOCK VIEW, AYRES END LANE, CHILDWICKBURY, ST. ALBANS
            "10024115888",  # FLAT AT ST ALBANS SCHOOL PAVILLION 162 HARPENDEN ROAD, ST ALBANS
            "200003633693",  # WOOD END, HATCHING GREEN, HARPENDEN
            "100081134635",  # PLAISTOWES FARM, NOKE LANE, ST. ALBANS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "AL4 0LD",
            "AL1 3NS",
            "AL3 5PD",
            "AL3 5PR",
            "AL1 4RJ",
            "AL4 0TP",
            # suspect
            "AL5 1AB",
            "AL5 1AA",
            "AL1 5NT",
            "AL5 2AB",
        ]:
            return None

        return super().address_record_to_dict(record)
