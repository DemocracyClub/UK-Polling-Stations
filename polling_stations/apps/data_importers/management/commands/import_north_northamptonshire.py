from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2024-05-02/2024-04-11T10:08:50.273571/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-11T10:08:50.273571/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
            "NN6 0FT",
            "NN18 9BD",
            "NN15 6YF",
            "NN18 8DZ",
            "NN15 6GQ",
            "NN14 1PF",
            "NN10 9NJ",
            "NN10 6EU",
            "NN8 1SH",
            "NN14 4EE",
            "NN14 3BY",
            "NN18 8RS",
            "NN29 7NL",
            "NN8 4WG",
            "NN10 9JD",
            "NN18 8QG",
            "NN8 3JX",
            "NN17 2HP",
            "NN14 4AJ",
            # suspect
            "NN9 6US",
            "NN9 6UQ",
            "NN14 2SP",
            "NN17 1FP",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode corrections from council:

        # Hope Methodist Church, Linnet Way Entrance, 19 High Street, Higham Ferrers NN10 0RW
        if record.polling_place_id == "30649":
            record = record._replace(polling_place_postcode="NN10 8DD")

        # The Autumn Centre, Counts Farm Road, Corby, NN18 8BH' (id: 30448)
        if record.polling_place_id == "30448":
            record = record._replace(polling_place_postcode="NN18 8BJ")

        # Cottingham/Middleton Village Hall, Berryfield Road, Cottingham, Market Harborough, LE16 8XD
        if record.polling_place_id == "30517":
            record = record._replace(polling_place_postcode="LE16 8XB")

        # Stanion Village Hall, Brigstock Road, Stanion, Kettering, NN14 1BX
        if record.polling_place_id == "30502":
            record = record._replace(polling_place_postcode="NN14 1BU")

        # East Carlton Cricket Club, East Carlton Park, East Carlton, Market Harborough, LE16 8YD
        if record.polling_place_id == "30524":
            record = record._replace(polling_place_postcode="LE16 8YF")
        return super().station_record_to_dict(record)
