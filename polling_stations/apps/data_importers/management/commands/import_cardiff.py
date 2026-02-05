from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2026-05-07/2026-02-05T10:36:48.817558/Democracy_Club__07May2026 Cardiff.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-05T10:36:48.817558/Democracy_Club__07May2026 Cardiff.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Community Suite, Llanishen Leisure Centre, Ty Glas Avenue, Llanishen, Cardiff
        if record.polling_place_id == "25858":
            # geocode was a way off, postcode was right, but found the building so here it is anyway
            record = record._replace(polling_place_uprn="10002526454")

        # The Church Hall, Kelston Road, Whitchurch, Cardiff
        if record.polling_place_id == "21205":
            record = record._replace(polling_place_uprn="200001850852")

        # St Mary`s Church Hall, Church Road, Cardiff, CF14 2ED
        # Council request to use below postcode, ignore the warning
        if record.polling_place_id == "25906":
            record = record._replace(
                polling_place_postcode="CF14 2DX", polling_place_uprn="10008903814"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100100110392",  # 10 SOMERSET COURT, BURNHAM AVENUE, LLANRUMNEY, CARDIFF
            "10008904957",  # OAK HOUSE, 340 NEWPORT ROAD, CARDIFF
            "10090488749",  # 456A COWBRIDGE ROAD EAST, CARDIFF
            "10092985344",  # FIRST FLOOR FLAT 452 COWBRIDGE ROAD EAST, CANTON, CARDIFF
            "10002507423",  # MAES Y LLECH FARM, RADYR, CARDIFF
            "100100896720",  # PARK HOUSE, MUIRTON ROAD, CARDIFF
        ]:
            return None

        if record.addressline6 in [
            # splits
            # looks wrong
            "CF11 6BN",
        ]:
            return None

        return super().address_record_to_dict(record)
