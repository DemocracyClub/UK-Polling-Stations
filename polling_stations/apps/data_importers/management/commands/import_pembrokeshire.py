from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "PEM"
    addresses_name = "2024-07-04/2024-06-17T09:55:22.022484/PEM_combined.csv"
    stations_name = "2024-07-04/2024-06-17T09:55:22.022484/PEM_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")
        if record.uprn in [
            "200003255203",  # LOWER FLAT, FERN HOUSE, WARREN STREET, TENBY
        ]:
            return None
        if record.housepostcode in [
            # split
            "SA73 2EB",
            "SA73 2EB",
            "SA62 4NJ",
            "SA62 3PW",
            "SA73 1RG",
            "SA72 6BE",
            "SA72 6BH",
            "SA73 1NR",
            "SA73 1BB",
            "SA62 5DB",
            "SA66 7QW",
            "SA62 3DA",
            "SA73 3HF",
            "SA73 3RA",
            "SA68 0QR",
            "SA67 8RY",
            "SA71 5BP",
            "SA62 5RJ",
            "SA71 4JT",
            "SA68 0XN",
            "SA62 5UD",
            "SA73 1RJ",
            "SA62 6TD",
            "SA62 5NL",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station change from council:
        # old: The Old Watersports Centre, Goodwick SA64 0DE
        # new: Goodwick Community School, Hill Street, Goodwick, SA64 0ET
        if record.pollingvenueid == "241":
            record = record._replace(
                pollingstationname="Goodwick Community School",
                pollingstationnumber="2014",
                pollingstationaddress_1="Hill Street",
                pollingstationaddress_2="Goodwick",
                pollingstationaddress_3="",
                pollingstationpostcode="SA64 0ET",
            )
        return super().station_record_to_dict(record)
