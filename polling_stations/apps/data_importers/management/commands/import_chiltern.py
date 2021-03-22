from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHN"
    addresses_name = "2021-03-18T18:05:02.131217/Bucks_dedupe.tsv"
    stations_name = "2021-03-18T18:05:02.131217/Bucks_dedupe.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081167219",  # 3 FIELDS END, NEW ROAD, PENN, HIGH WYCOMBE
            "100081184513",  # THE GRANARY, WEEDON HILL, HYDE HEATH, AMERSHAM
            "10013781220",  # 2 LOWER HUNDRIDGE FARM COTTAGE, MISSENDEN ROAD, CHESHAM
            "100081184512",  # 1 LOWER HUNDRIDGE FARM COTTAGE, MISSENDEN ROAD, CHESHAM
            "10095500123",  # MOBILE HOME ST GEORGES HALL JASONS HILL, CHESHAM
            "10013781402",  # THE CLOCKHOUSE NORTH LODGE LOWER ROAD, CHALFONT ST PETER
            "10013780859",  # 44A HIGH STREET, GREAT MISSENDEN
            "10013777238",  # HAWTHORN FARM BARN HAWTHORN FARM CHESHAM ROAD, HYDE END
        ]:
            return None

        if record.addressline6 in [
            "SL9 9JH",
            "HP16 0HR",
            "SL9 0ED",
            "HP8 4QT",
            "HP8 4DF",
            "SL9 9FH",
        ]:
            return None

        return super().address_record_to_dict(record)
