from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = (
        "2026-08-13/2026-07-28T14:10:29.318851/TEN - DC - Polling District CBE.csv"
    )
    stations_name = (
        "2026-08-13/2026-07-28T14:10:29.318851/TEN - DC Polling Staions UKPBE.csv"
    )
    elections = ["2026-08-13"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if (
            record.uprn
            in [
                "10096724996",  # SWEET PEA, MILL LANE, THORPE-LE-SOKEN, CLACTON-ON-SEA
                "100091268553",  # 163 MEADOW VIEW PARK, ST. OSYTH ROAD, LITTLE CLACTON, CLACTON-ON-SEA
            ]
        ):
            return None

        if record.postcode in [
            # suspect
            "CO15 1HX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station name change from council for:
        # Cann Hall Primary School - Hall in School Constable Avenue Clacton-on-Sea Essex
        if record.stationcode in [
            "6",
            "7",
        ]:
            record = record._replace(
                placename="Little Jimmys Preschool (Cann Hall Primary School) - Hall in School Constable Avenue Clacton-on-Sea Essex"
            )
        return super().station_record_to_dict(record)
