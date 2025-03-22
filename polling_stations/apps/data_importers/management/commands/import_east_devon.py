from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = (
        "2025-05-01/2025-03-17T14:58:28.088039/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-17T14:58:28.088039/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094722867",  # MOLLYS COTTAGE SNODWELL FARM POST LANE, COTLEIGH
            "10093128988",  # CARAVAN 2 GREENDALE LANE, CLYST ST MARY
            "10094722905",  # LITTLE HAYES, SIDMOUTH ROAD, AYLESBEARE, EXETER
            "100040154030",  # OLD BARN FARM, LODGE LANE, AXMINSTER
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "EX14 4SE",
            # suspect
            "EX4 0AB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Postcode in wrong columns for:  Old Picture House, Harbour Road, Seaton, EX12 2LZ
        if record.polling_place_id == "16300":
            record = record._replace(
                polling_place_postcode=record.polling_place_address_3
            )

        return super().station_record_to_dict(record)
