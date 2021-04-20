from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = (
        "2021-03-30T10:12:37.728458/Rhondda polling_station_export-2021-03-30.csv"
    )
    stations_name = (
        "2021-03-30T10:12:37.728458/Rhondda polling_station_export-2021-03-30.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "121":
            # ST DAVIDS CHURCH, LLANTRISANT ROAD, GROESFAEN, PONTYCLUN
            # "CF72 8NU" → "CF72 8NS"
            # Source: https://www.churchinwales.org.uk/en/structure/church/4123/
            record = record._replace(pollingstationpostcode="CF72 8NS")

        if record.pollingstationnumber == "94":
            # CILFYNYDD & NORTON BRIDGE COMMUNITY CENTRE, CILFYNYDD ROAD, …
            # Was "CF37 3NR", but that's not on Cilfyndd Road
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CF44 9DT",
            "CF44 0PD",
            "CF37 3EW",
            "CF37 4DX",
            "CF38 2SA",
            "CF37 2HL",
            "CF37 1UA",
            "CF37 1LD",
            "CF39 8AT",
            "CF39 8FA",
            "CF42 6LX",
        ]:
            return None  # split

        if record.housepostcode in [
            "CF72 8LQ",  # overlapping districts; looks odd
        ]:
            return None

        uprn = getattr(record, self.residential_uprn_field).strip()

        if uprn in [
            "100100774832",  # improbable distance; crosses other district
        ]:
            return None

        return super().address_record_to_dict(record)
