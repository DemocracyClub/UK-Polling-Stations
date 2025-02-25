from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUC"
    addresses_name = (
        "2025-05-01/2025-02-13T17:41:34.465191/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-13T17:41:34.465191/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000796229",  # MOORGATE COTTAGE, MOOR END, FRIETH, HENLEY-ON-THAMES
            "10090192931",  # MOBILE HOME AT STABLES AND PADDOCK WILLETTS LANE, DENHAM
            "766297724",  # RYE HOUSE THE HOLLOWAY, DRAYTON BEAUCHAMP
        ]:
            return None

        if record.addressline6 in [
            # split
            "SL9 9JH",
            "HP8 4QT",
            "HP23 6NG",
            "HP8 4DF",
            "SL0 0DB",
            "SL9 9FH",
            "HP5 3BD",
            "HP18 0RU",
            "RG9 6JH",
            "HP18 9UJ",
            # suspect
            "HP12 3HP",  # MCLELLAN PLACE
            "SL3 6QH",  # CROMWELLS COURT
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Correction from council: St John’s Methodist Church, 60 Woodside Avenue to Restore Hope Amersham Hall, 60 Woodside Avenue
        if record.polling_place_id == "42155":
            record = record._replace(polling_place_name="Restore Hope Amersham Hall")

        return super().station_record_to_dict(record)
