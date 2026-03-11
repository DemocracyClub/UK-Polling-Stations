from data_importers.management.commands import BaseFcsDemocracyClubApiImporter


class Command(BaseFcsDemocracyClubApiImporter):
    council_id = "TES"
    elections = ["2026-05-07"]
    fcs_election_id = 99

    def station_record_to_dict(self, record):
        station_id = record.get(self.station_id_field)

        # add point for: Weir Link Community Centre, 33 Weir Road, London, SW12 0NU
        if (
            station_id
            in [
                14725,  # Personal Best Education Lounge The Mountbatten School Whitenap Lane Romsey
                14747,  # Sports Pavilion, Abbottswood Sports Ground Cutforth Way Romsey Hampshire
                14737,  # Portakabin at Sports Field Kiel Drive Saxon Fields Andover Hampshire
            ]
        ):
            record["longitude"] = 0
            record["latitude"] = 0

        return super().station_record_to_dict(record)

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")
    #
    #     if uprn in [
    #         "200000704153",  # WOODLANDS, LOCKES DROVE, PILL HEATH, ANDOVER
    #     ]:
    #         return None
    #     if record.addressline6 in [
    #         # split
    #         "SP11 0HB",
    #         "SO51 6EB",
    #     ]:
    #         return None
    #     return super().address_record_to_dict(record)
