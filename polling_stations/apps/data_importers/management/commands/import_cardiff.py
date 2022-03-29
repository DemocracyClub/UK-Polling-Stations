from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2022-05-05/2022-03-29T16:13:09.124728/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T16:13:09.124728/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Community Suite, Llanishen Leisure Centre, Ty Glas Avenue, Llanishen, Cardiff
        if record.polling_place_id == "17968":
            # geocode was a way off, postcode was right, but found the building so here it is anyway
            record = record._replace(polling_place_uprn="10002526454")

        # Canolfan Beulah, (Church Community Centre), Beulah Crossroads, Rhiwbina, Cardiff
        if record.polling_place_id == "18139":
            # postcode was CF14 6AX, which didn't geocode
            record = record._replace(
                polling_place_postcode="CF14 6LT", polling_place_uprn="200001485221"
            )

        # The Church Hall, Kelston Road, Whitchurch, Cardiff
        if record.polling_place_id == "18273":
            record = record._replace(polling_place_uprn="200001850852")

        # St Mary`s Church Hall, Church Road, Cardiff
        if record.polling_place_id == "18480":
            record = record._replace(
                polling_place_postcode="CF14 2AA", polling_place_uprn="10008903814"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["CF24 2DG"]:
            return None  # split

        return super().address_record_to_dict(record)
