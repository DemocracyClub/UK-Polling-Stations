from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "LBH"
    elections = ["2026-05-07"]
    fcs_election_id = 52

    def station_record_to_dict(self, record):
        station_id = record.get(self.station_id_field)

        # add point for: Weir Link Community Centre, 33 Weir Road, London, SW12 0NU
        if station_id == 11449:
            record["longitude"] = -0.139770
            record["latitude"] = 51.446899

        # add point for: Elmgreen Secondary School, Elmcourt Road, London, SE27 9BZ
        if station_id == 11311:
            record["longitude"] = -0.102054
            record["latitude"] = 51.438839

        return super().station_record_to_dict(record)
