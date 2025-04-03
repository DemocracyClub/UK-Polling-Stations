from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2025-05-01/2025-03-28T08:38:25.150612/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-28T08:38:25.150612/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031061536",  # STABLE COTTAGE, HEADLANDS, KETTERING
            "100031076255",  # THE SHEILINGS STOKE ALBANY ROAD, DESBOROUGH
            "10094095301",  # ASH TREE FARM, STOKE ALBANY ROAD, DESBOROUGH, KETTERING
            "10007877421",  # CARAVAN 1 DESBOROUGH ROAD, BRAYBROOKE
            "100031081643",  # THE LODGE SUTTON LANE, DINGLEY
            "10093005483",  # 2 BOUGHTON LANE, RAUNDS, WELLINGBOROUGH
        ]:
            return None
        if record.addressline6 in [
            # split
            "NN10 6EU",
            "NN6 0FT",
            "NN8 1SH",
            "NN15 5GL",
            "NN8 3JX",
            "NN10 9NJ",
            "NN18 0LG",
            "NN18 9BD",
            "NN10 9JD",
            "NN14 1PF",
            "NN18 8DZ",
            "NN14 3BY",
            "NN8 1HG",
            "NN17 2HP",
            "NN8 4WG",
            "NN18 8QG",
            "NN14 4AJ",
            # suspect
            "NN9 6UQ",
            "NN14 2SP",
            "NN17 4BA",
            "NN17 3FG",
            "NN17 3FF",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: The Autumn Centre, Counts Farm Road, Corby, NN18 8BJ
        if record.polling_place_id == "34364":
            record = record._replace(polling_place_postcode="NN18 8BH")

        return super().station_record_to_dict(record)
