from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ARU"
    addresses_name = (
        "2023-05-04/2023-03-03T11:00:12.161577/Democracy_Club__04May2023 (2).tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-03T11:00:12.161577/Democracy_Club__04May2023 (2).tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023374366",  # CORNERWAYS APARTMENT, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
            "100061728945",  # THE MALTHOUSE, WEAVERS HILL, ANGMERING, LITTLEHAMPTON
            "10023374778",  # THE RANCH, WATER LANE, ANGMERING, LITTLEHAMPTON
            "10091568678",  # THE LODGE, SELDEN LANE, PATCHING, WORTHING
            "200002712986",  # 149 SELDEN LANE, PATCHING, WORTHING
            "10023375171",  # PLOT 3 OVAL MOTOR RACING TRACK WATER LANE, ANGMERING
            "10091567667",  # 7 WEST MEADS DRIVE, BOGNOR REGIS
            "100061686788",  # SOUTHDOWN COTTAGE, YAPTON LANE, WALBERTON, ARUNDEL
            "200002715229",  # GREEN DOORS LODGE, LONDON ROAD, ARUNDEL
            "10000190927",  # MICHEL GROVE HOUSE, PATCHING, WORTHING
        ]:
            return None

        if record.addressline6 in [
            "PO21 1JB",  # splits
            "BN16 4QT",  # ambiguous data @ Angmering, Littlehampton, West Sussex
            "BN16 4QZ",  # ambiguous data @ Angmering, Littlehampton, West Sussex
            "BN13 3UG",  # TITNORE LANE, PATCHING, WORTHING
        ]:
            return None

        return super().address_record_to_dict(record)
