from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TAW"
    addresses_name = (
        "2026-06-25/2026-05-18T09:29:35.684728/Democracy_Club__25June2026.tsv"
    )
    stations_name = (
        "2026-06-25/2026-05-18T09:29:35.684728/Democracy_Club__25June2026.tsv"
    )
    elections = ["2026-06-25"]
    csv_delimiter = "\t"

    # maintaining exclusions as comments through by-election

    # # def address_record_to_dict(self, record):
    # #     uprn = record.property_urn.strip().lstrip("0")

    # #     if uprn in [
    # #         "394037200",  # 105A COMBERFORD ROAD, TAMWORTH, B79 8PQ
    # #         "394017153",  # 248 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394017141",  # 236 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394017147",  # 242 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394017183",  # 278 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394017189",  # 284 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394017177",  # 272 MASEFIELD DRIVE, TAMWORTH, B79 8JF
    # #         "394030583",  # 29B MICA CLOSE, TAMWORTH, B77 4DR
    # #         "394027534",  # 100 WOODHOUSE LANE, TAMWORTH, B77 3AF
    # #         "394027533",  # 102 WOODHOUSE LANE, TAMWORTH, B77 3AF
    # #     ]:
    # #         return None

    #     return super().address_record_to_dict(record)
