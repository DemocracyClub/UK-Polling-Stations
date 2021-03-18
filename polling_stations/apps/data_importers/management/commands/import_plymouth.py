from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = "2021-03-17T12:57:39.682268/Plymouth Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-17T12:57:39.682268/Plymouth Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Chaddlewood Farm Community Centre 80 Chaddlewood District Centre Glen Road Plympton Plymouth PL7 2XS
        if record.polling_place_id == "4959":
            record = record._replace(polling_place_easting="256137")
            record = record._replace(polling_place_northing="56152")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070771403",  # 53 KENSINGTON ROAD, PLYMOUTH
            "100040454247",  # FLAT 2, 24 DRINA LANE, PLYMOUTH
            "10012062433",  # FLAT 1, 24 DRINA LANE, PLYMOUTH
            "100040415376",  # FLAT 2 METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
            "100040480583",  # 1A CROWNHILL ROAD, PLYMOUTH
            "100040439817",  # 1B CROWNHILL ROAD, PLYMOUTH
            "100040480569",  # 30 RIDGE ROAD, PLYMPTON, PLYMOUTH
            "10070769227",  # THE JACK RABBIT, 8 BRACKEN LANE, DERRIFORD, PLYMOUTH
            "10070771404",  # CARETAKERS FLAT METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
            "100040480581",  # FLAT A ELFORDE HOUSE BLANDFORD ROAD, PLYMOUTH
            "100040480585",  # THE HOLLOW, TAMERTON FOLIOT ROAD, PLYMOUTH
            "100040480568",  # POINT COTTAGE, SALTRAM, PLYMOUTH
            "100040480573",  # 26 RIDGE ROAD, PLYMPTON, PLYMOUTH
            "100040480578",  # 28 RIDGE ROAD, PLYMPTON, PLYMOUTH
            "100040480580",  # 184 RINGMORE WAY, PLYMOUTH
            "100040434952",  # FORDER COTTAGE, FORDER VALLEY ROAD, PLYMOUTH
            "10091561767",  # 162 RINGMORE WAY, PLYMOUTH
            "10012058853",  # 168 RINGMORE WAY, PLYMOUTH
            "100040480571",  # 174 RINGMORE WAY, PLYMOUTH
            "100040493091",  # 176 RINGMORE WAY, PLYMOUTH
            "10091564004",  # 182 RINGMORE WAY, PLYMOUTH
            "10091564022",  # 172 RINGMORE WAY, PLYMOUTH
            "100040480587",  # 166 RINGMORE WAY, PLYMOUTH
            "10091564003",  # 164 RINGMORE WAY, PLYMOUTH
            "10070769306",  # 178 RINGMORE WAY, PLYMOUTH
            "100040480576",  # 180 RINGMORE WAY, PLYMOUTH
            "100040429061",  # 216 CULVER WAY, PLYMOUTH
            "10012061586",  # GROUND FLOOR FLAT 316 SALTASH ROAD, KEYHAM, PLYMOUTH
        ]:
            return None

        if record.addressline6 in [
            "PL4 7HE",
            "PL4 7QB",
            "PL7 1AA",
            "PL2 2DQ",
            "PL6 5JZ",
            "PL3 6EP",
            "PL7 1PD",
        ]:
            return None

        return super().address_record_to_dict(record)
