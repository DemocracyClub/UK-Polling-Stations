from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "MRT"
    addresses_name = "2026-05-07/2026-03-24T14:49:49.615691/Democracy Club - Idox_2026-03-24 13-07.csv"
    stations_name = "2026-05-07/2026-03-24T14:49:49.615691/Democracy Club - Idox_2026-03-24 13-07.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "CR4 2JR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # council station name change for: Ravensbury Residents Room, Ravensbury Grove, Mitcham, CR4 4DL
        if record.pollingstationnumber == "29":
            record = record._replace(
                pollingstationname="Portacabin Ravensbury Residents Room"
            )

        # council station coordinates change for: Cherry Red Records Stadium, Plough Lane, London, SW17 0NR
        if record.pollingstationnumber == "88":
            record = record._replace(
                pollingvenueeasting="526150", pollingvenuenorthing="171722"
            )

        return super().station_record_to_dict(record)
