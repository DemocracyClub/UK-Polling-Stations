from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2026-08-13/2026-08-10T13:27:31.372593/Democracy_Club__13August2026.tsv"
    )
    stations_name = (
        "2026-08-13/2026-08-10T13:27:31.372593/Democracy_Club__13August2026.tsv"
    )
    elections = ["2026-08-13"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "83190068",  # 5 MOOR TOP FARM, MOOR TOP LANE, FLOCKTON MOOR, WAKEFIELD
            "83183588",  # 1 HARE PARK LANE, LIVERSEDGE
            "83157946",  # HIGHBRIDGE LODGE, HIGHBRIDGE, SCISSETT, HUDDERSFIELD
            "83050605",  # 67 GLENEAGLES WAY, HUDDERSFIELD
            "83050604",  # 69 GLENEAGLES WAY, HUDDERSFIELD
            "83050607",  # 71 GLENEAGLES WAY, HUDDERSFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "WF17 7ND",
        ]:
            return None

        return super().address_record_to_dict(record)
