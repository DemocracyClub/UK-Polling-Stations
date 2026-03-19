from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "NUN"
    addresses_name = "2026-05-07/2026-03-05T11:53:55.856561/PropertyPostCodePollingStationWebLookup-2026-03-05.TSV"
    stations_name = "2026-05-07/2026-03-05T11:53:55.856561/PropertyPostCodePollingStationWebLookup-2026-03-05.TSV"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.uprn in [
            "100071496605",  # BRAMCOTE FIELDS FARM, LUTTERWORTH ROAD, BRAMCOTE, NUNEATON
            "100071235227",  # MEADOW FARM, LUTTERWORTH ROAD, BRAMCOTE, NUNEATON
        ]:
            return None

        if record.postcode in [
            # split
            "CV10 9QF",
            "CV11 4NW",
            "CV11 6NL",
            "CV11 6JE",
            # suspect
            "CV12 9HJ",
            "CV10 0PL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode column switch for: Poplars Farm Cabin, 45 The Long Shoot, Nuneaton
        if record.pollingplaceid == "11087":
            record = record._replace(pollingplaceaddress7=record.pollingplaceaddress6)

        # Correct postcode for: Town Hall, Nuneaton & Bedworth Borough Council, Coton Road
        if record.pollingplaceid == "11049":
            record = record._replace(pollingplaceaddress7="CV11 5AA")

        return super().station_record_to_dict(record)
