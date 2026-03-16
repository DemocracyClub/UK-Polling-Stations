from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "TAN"
    addresses_name = "2026-05-07/2026-03-16T13:01:38.577321/Democracy Club - Idox_2026-03-16 12-02.csv"
    stations_name = "2026-05-07/2026-03-16T13:01:38.577321/Democracy Club - Idox_2026-03-16 12-02.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "200000141057",  # MOAT FARM, ARDENRUN, LINGFIELD, RH7 6LN
                "100062498468",  # LONG ACRES CARAVAN & CAMPING PARK, NEWCHAPEL ROAD, LINGFIELD, RH7 6LE
                "10007910403",  # SWEET BRIAR FARM, NEWCHAPEL ROAD, LINGFIELD, RH7 6BL
                "200000141065",  # OLD MOAT BARN, ARDENRUN, LINGFIELD
                "200000140050",  # SURREY BEECHES, WESTERHAM ROAD, WESTERHAM
                "200000140051",  # SURREY BEECHES WEST, WESTERHAM ROAD, WESTERHAM
                "100061586276",  # CLOVERLAY, ROCKFIELD ROAD, OXTED
                "100061586681",  # 39A STATION ROAD EAST, OXTED
            ]
        ):
            return None

        if record.postcode in [
            "CR6 9LB",  # split
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removing obviously wrong coords (location in the water), postcode geolocation is fine
        # Bletchingley Village Hall, 78 & 78A High Street, Bletchingley, Redhill, RH1 4PA
        if record.pollingstationnumber in ["1", "2"]:
            record = record._replace(pollingvenuenorthing=0, pollingvenueeasting=0)

        # Caterham Hill Library, Caterham Hill Library, Westway, Caterham, CR3 5TP
        if record.pollingstationnumber in ["29", "30"]:
            record = record._replace(pollingvenuenorthing=0, pollingvenueeasting=0)

        return super().station_record_to_dict(record)
