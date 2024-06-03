from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAS"
    addresses_name = (
        "2024-07-04/2024-06-03T10:19:06.526538/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-03T10:19:06.526538/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Bannatyne Spa Hotel (Montgomerie Suite), Battle Road, St Leonards on Sea, East Sussex
        if record.polling_place_id == "1290":
            # postcode was out-of-area
            record = record._replace(
                polling_place_postcode="TN38 8EZ", polling_place_uprn="10070602485"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062575170",  # FLAT 1 SIDNEY HOUSE 354B OLD LONDON ROAD, HASTINGS
            "100062575171",  # FLAT 2 SIDNEY HOUSE 354B OLD LONDON ROAD, HASTINGS
            "100062575172",  # FLAT 3 SIDNEY HOUSE 354B OLD LONDON ROAD, HASTINGS
            "100062577569",  # 120 BATTLE ROAD, ST. LEONARDS-ON-SEA
            "100062580304",  # SANCTUAIRE, CROWHURST ROAD, ST. LEONARDS-ON-SEA
        ]:
            return None

        if record.addressline6 in [
            # split
            "TN38 9BP",
            "TN38 0YJ",
            "TN38 0PB",
            "TN34 1TB",
        ]:
            return None
        return super().address_record_to_dict(record)
