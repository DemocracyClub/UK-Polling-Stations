from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROH"
    addresses_name = (
        "2026-05-07/2026-04-24T10:10:06.338529/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-24T10:10:06.338529/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002668563",  # HOME FARM BARN, ETCHINGHAM
            "10002651836",  # LUDPIT COTTAGE, LUDPIT LANE, ETCHINGHAM
            "10002668412",  # COWFIELD COTTAGE, BODIAM, ROBERTSBRIDGE
            "10090508857",  # 2 OCKHAM MEWS, BODIAM, ROBERTSBRIDGE
            "10090507447",  # 1 OCKHAM MEWS, BODIAM, ROBERTSBRIDGE
            "10002662323",  # DYKES FARM, EWHURST GREEN, ROBERTSBRIDGE
            "100060089232",  # 49 ELLERSLIE LANE, BEXHILL-ON-SEA
            "100062584403",  # HIGHWOODS GOLF CLUB LTD, 47 ELLERSLIE LANE, BEXHILL-ON-SEA
        ]:
            return None

        if record.addressline6 in [
            "TN40 2AG",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
