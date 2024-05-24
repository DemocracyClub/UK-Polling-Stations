from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = (
        "2024-07-04/2024-05-24T14:37:10.506351/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-24T14:37:10.506351/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000162928",  # 2 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "200000162927",  # 1 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "10000829965",  # 2 STABLE COTTAGE RUSPER ROAD, CAPEL
            "10000829964",  # 1 STABLE COTTAGE RUSPER ROAD, CAPEL
            "10000828494",  # ARNWOOD FARM COTTAGE RUSPER ROAD, NEWDIGATE
            "200000168361",  # THE CARAVAN PACHESHAM FARM RANDALLS ROAD, LEATHERHEAD
            "200000160843",  # ROARING HOUSE FARM, FETCHAM DOWNS, FETCHAM, LEATHERHEAD
            "100062137867",  # EAST STANDON LODGE, STANE STREET, OCKLEY, DORKING
            "100062495967",  # THE TOWER, RUSPER ROAD, CAPEL, DORKING
            "100062137505",  # SOUTH LODGE DENBIES, RANMORE ROAD, DORKING
            "10000824831",  # RIVENDALE FARM RUSPER ROAD, CAPEL
            "100061426171",  # KEEPERS COTTAGE, RANMORE COMMON ROAD, WESTHUMBLE, DORKING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "KT21 2LY",
            # looks wrong
            "KT22 9BP",
            "RH5 4DW",
        ]:
            return None

        return super().address_record_to_dict(record)
