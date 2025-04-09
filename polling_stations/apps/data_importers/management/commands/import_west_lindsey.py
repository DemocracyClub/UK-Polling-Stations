from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLI"
    addresses_name = (
        "2025-05-01/2025-03-27T15:45:49.934679/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-27T15:45:49.934679/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013815969",  # WEST VIEW FARM, STOW PARK, LINCOLN
            "10013812180",  # 1 NETTLETON PARK MOORTOWN ROAD, NETTLETON, MARKET RASEN
        ]:
            return None

        if record.addressline6 in [
            # split
            "DN21 1TU",
            "LN1 2DU",
            "DN21 1HL",
            "LN8 3SU",
            # suspect
            "LN8 6JA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station coords from council for:
        # Drawing Room, Hemswell Court, Lancaster Green, Hemswell Cliff,  Gainsborough, DN21 5TQ
        if record.polling_place_id == "13465":
            record = record._replace(polling_place_uprn="10013810899")
        # The Village Hall, Bishop Norton Road, Glentham LN8 2EU
        if record.polling_place_id == "13319":
            record = record._replace(polling_place_uprn="100032253643")

        return super().station_record_to_dict(record)
