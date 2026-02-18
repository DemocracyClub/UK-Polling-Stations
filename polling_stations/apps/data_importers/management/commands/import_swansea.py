from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SWA"
    addresses_name = "2026-05-07/2026-02-19T10:30:42.465310/SWA_combined.csv"
    stations_name = "2026-05-07/2026-02-19T10:30:42.465310/SWA_combined.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10094784277",  # ROOM A 116 OLDWAY CENTRE 39 HIGH STREET, CITY CENTRE, SWANSEA, SA1 1LD
                "100100401496",  # 37A HIGH STREET, GORSEINON, SWANSEA, SA4 4BT
                "10011729995",  # ROSE COTTAGE UNCLASSIFIED SECTION-Y2117, OXWICH, SWANSEA, SA3 1LN
                "10010058515",  # THE LAUNDRY MIDDLETON HALL UNCLASSIFIED SECTION-Y2400, RHOSSILI, SWANSEA,SA3 1PJ
            ]
        ):
            return None

        if record.postcode in [
            # split
            "SA6 6DS",
            "SA1 6NQ",
            "SA3 3JS",
            "SA4 3QX",
            "SA1 8PN",
            "SA5 7HY",
            # suspect
            "SA2 0EU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Llangyfelach Church Hall Swansea Road Llangyfelach Swansea
        if self.get_station_hash(record) == "7-llangyfelach-church-hall":
            record = record._replace(pollingstationpostcode="SA5 7JD")

        return super().station_record_to_dict(record)
