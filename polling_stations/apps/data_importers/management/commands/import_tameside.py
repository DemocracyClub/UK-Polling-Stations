from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAM"
    addresses_name = (
        "2026-02-26/2026-02-09T10:52:27.340729/Democracy_Club__26February2026.tsv"
    )
    stations_name = (
        "2026-02-26/2026-02-09T10:52:27.340729/Democracy_Club__26February2026.tsv"
    )
    elections = ["2026-02-26"]
    csv_delimiter = "\t"

    # Maintaining some exclusions are comments here through a by-election
    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096633108",  # 1 TAYLOR STREET, DENTON, MANCHESTER
            "10096633109",  # 3 TAYLOR STREET, DENTON, MANCHESTER
            "100012488220",  # 105 THORNLEY LANE SOUTH, STOCKPORT
            # "10090073761",  # 19A WELLINGTON STREET, ASHTON-UNDER-LYNE
            # "10090073763",  # 21A WELLINGTON STREET, ASHTON-UNDER-LYNE
            # "10090073764",  # 21B WELLINGTON STREET, ASHTON-UNDER-LYNE
            # "200004419358",  # FLAT 2 34 HUDSON ROAD, HYDE
            # "200004410061",  # FLAT 2 2 OLD HALL LANE, MOTTRAM
            # "100012777909",  # HOPKINS FARM COTTAGE, ARLIES LANE, STALYBRIDGE
            # "100012777908",  # HOPKINS COTTAGE, ARLIES LANE, STALYBRIDGE
            # "100011545502",  # 2 JOHN STREET, DENTON, MANCHESTER
            # "10014255906",  # THE HOLLIES BUNGALOW, BOYDS WALK, DUKINFIELD
            # "200002857633",  # PORTLAND BASIN MARINA, LOWER ALMA STREET, DUKINFIELD
            # "10014258331",  # ARMSTRONGS OFFICE FURNITURE, 29 PENNY MEADOW, ASHTON-UNDER-LYNE
        ]:
            return None

        if (
            record.addressline6
            in [
                # suspect
                # "SK14 4RD",
            ]
        ):
            return None
        return super().address_record_to_dict(record)
