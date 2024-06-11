from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2024-07-04/2024-06-11T14:53:16.766847/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-11T14:53:16.766847/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031061536",  # STABLE COTTAGE, HEADLANDS, KETTERING
            "100031076255",  # THE SHEILINGS STOKE ALBANY ROAD, DESBOROUGH
            "10094095301",  # ASH TREE FARM, STOKE ALBANY ROAD, DESBOROUGH, KETTERING
            "10007877421",  # CARAVAN 1 DESBOROUGH ROAD, BRAYBROOKE
            "100031081643",  # THE LODGE SUTTON LANE, DINGLEY
            "10008566697",  # HARPERS BROOK, 17 CHARTER COURT, CORBY
        ]:
            return None
        if record.addressline6 in [
            # split
            "NN10 9NJ",
            "NN18 8DZ",
            "NN14 1PF",
            "NN8 1SH",
            "NN17 2HP",
            "NN6 0FT",
            "NN8 3JX",
            "NN29 7NL",
            "NN10 9JD",
            "NN8 4WG",
            "NN18 9BD",
            "NN15 6GQ",
            "NN15 6YF",
            "NN10 6EU",
            "NN14 4EE",
            "NN18 8QG",
            "NN15 5GL",
            "NN18 8RS",
            "NN14 4AJ",
            "NN14 3BY",
            # suspect
            "NN9 6US",
            "NN9 6UQ",
            "NN14 2SP",
            "NN17 1FP",
        ]:
            return None
        return super().address_record_to_dict(record)
