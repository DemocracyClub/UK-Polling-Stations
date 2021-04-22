from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = "2021-04-22T13:51:28.820490/NewDemocracy_Club__06May2021.tsv"
    stations_name = "2021-04-22T13:51:28.820490/NewDemocracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310030097",  # FLAT 2 EASTERN COURT EASTERN AVENUE, READING
            "310045307",  # FLAT 1 EASTERN COURT EASTERN AVENUE, READING
            "310084262",  # THE GARDEN FLAT 191 KINGS ROAD, READING
            "310077277",  # 191 KINGS ROAD, READING
            "310078045",  # FLAT 3, 29A KENDRICK ROAD, READING
            "310078050",  # FLAT 8, 29A KENDRICK ROAD, READING
            "310078044",  # FLAT 2, 29A KENDRICK ROAD, READING
            "310078049",  # FLAT 7, 29A KENDRICK ROAD, READING
            "310078047",  # FLAT 5, 29A KENDRICK ROAD, READING
            "310078043",  # FLAT 1, 29A KENDRICK ROAD, READING
            "310078048",  # FLAT 6, 29A KENDRICK ROAD, READING
            "310078046",  # FLAT 4, 29A KENDRICK ROAD, READING
            "310084858",  # FLAT 3, 69 NORTHUMBERLAND AVENUE, READING
            "310084859",  # FLAT 4, 69 NORTHUMBERLAND AVENUE, READING
            "310084857",  # FLAT 2, 69 NORTHUMBERLAND AVENUE, READING
            "310084856",  # FLAT 1, 69 NORTHUMBERLAND AVENUE, READING
            "310075515",  # 14A BASINGSTOKE ROAD, READING
            "310037159",  # 12 DARTMOUTH TERRACE, LONDON ROAD, READING
        ]:
            return None

        if record.addressline6 in [
            "RG1 6DJ",
            "RG1 7EY",
            "RG4 5BB",
            "RG2 8JH",
            "RG1 5RU",
            "RG1 5PZ",
            "RG1 5BY",
            "RG4 7TQ",
            "RG1 6AB",
            "RG4 8ES",
            "RG2 7EZ",
            "RG1 4AP",
            "RG30 3DZ",
        ]:
            return None

        return super().address_record_to_dict(record)
