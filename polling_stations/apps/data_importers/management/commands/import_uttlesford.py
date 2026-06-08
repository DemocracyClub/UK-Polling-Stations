from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "UTT"
    addresses_name = (
        "2026-06-25/2026-06-08T10:58:59.549709/Democracy_Club__25June2026.tsv"
    )
    stations_name = (
        "2026-06-25/2026-06-08T10:58:59.549709/Democracy_Club__25June2026.tsv"
    )
    elections = ["2026-06-25"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200004260145",  # THREE GABLES, NEW COMMON, LITTLE HALLINGBURY, BISHOP'S STORTFORD, CM22 7RT
                "10090836555",  # THREE ACRES, NEW BARN LANE, LITTLE HALLINGBURY, BISHOP'S STORTFORD, CM22 7PR
                "10002182834",  # ANNEXE AT PLEDGDON LODGE BRICK END ROAD, HENHAM, CM22 6BN
                "10094832340",  # THE CART LODGE, ROOKERY LANE, WENDENS AMBO, SAFFRON WALDEN, CB11 4JS
                "200004270665",  # THE OLD SCHOOL HOUSE STATION ROAD, LITTLE DUNMOW
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "CM22 6FG",
            "CM22 6TW",
            "CB11 3US",
            "CM6 2GE",
        ]:
            return None

        return super().address_record_to_dict(record)
