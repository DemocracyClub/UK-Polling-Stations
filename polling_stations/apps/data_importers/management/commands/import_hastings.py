from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAS"
    addresses_name = (
        "2022-05-05/2022-04-04T12:50:30.594021/Democracy_Club__05May2022-2.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-04T12:50:30.594021/Democracy_Club__05May2022-2.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Bannatyne Spa Hotel (Montgomerie Suite), Battle Road, St Leonards on Sea, East Sussex
        if record.polling_place_id == "1004":
            # postcode was out-of-area
            record = record._replace(
                polling_place_postcode="TN38 8EZ", polling_place_uprn="10070602485"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TN34 3JE",
            "TN37 7QX",
            "TN38 9BP",
            "TN38 0YJ",
            "TN34 1TB",
            "TN38 0PB",
        ]:
            return None  # split
        return super().address_record_to_dict(record)
