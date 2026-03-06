from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPP"
    addresses_name = "2026-05-07/2026-02-09T13:51:53.694969/Democracy_Club__07May2026.tsv pre noms.tsv"
    stations_name = "2026-05-07/2026-02-09T13:51:53.694969/Democracy_Club__07May2026.tsv pre noms.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Adding Missing UPRNs from the council for:
        # Kingsley Hall, 5 Austen Close Loughton
        if record.polling_place_id == "3892":
            record = record._replace(polling_place_uprn="100091479336")
        # Ongar Youth Centre, The Gables, Fyfield Road
        if record.polling_place_id == "3900":
            record = record._replace(polling_place_uprn="10022854094")
        # The Black Swan Broadley Common
        if record.polling_place_id == "3873":
            record = record._replace(polling_place_uprn="100091477706")
        # Victory Hall, Hainault Road, Chigwell
        if record.polling_place_id == "3848":
            record = record._replace(polling_place_uprn="100091480121")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10012157511",  # WALLED GARDEN HOUSE, EPPING
                "10012157510",  # TIMBER LODGE, EPPING
                "100091477396",  # SCHOOL HOUSE, KING HAROLD SCHOOL, BROOMSTICK HALL ROAD, WALTHAM ABBEY
                "100091251326",  # THE PANTILES, DUNMOW ROAD, FYFIELD, ONGAR
                "100091251152",  # THATCHED COTTAGE, BIRDS GREEN, WILLINGALE, ONGAR
                "100091247388",  # BROOKSIDE, GRAVEL LANE, CHIGWELL
                "10022857825",  # CARAVAN 2 MOSS NURSERY SEDGE GREEN, ROYDON, HARLOW
                "200002755166",  # GARDEN COTTAGE, NURSERY ROAD, LOUGHTON
                "100090505679",  # 94A HIGH ROAD, LOUGHTON
                "10012166253",  # 1 BUSH HALL COTTAGES, THRESHERS BUSH, HARLOW
                "10012166254",  # 2 BUSH HALL COTTAGES, THRESHERS BUSH, HARLOW
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "CM5 0HP",
            "CM5 9LY",
        ]:
            return None

        return super().address_record_to_dict(record)
