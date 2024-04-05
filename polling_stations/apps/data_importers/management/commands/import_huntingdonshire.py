from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = (
        "2024-05-02/2024-03-05T14:28:58.853244/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-05T14:28:58.853244/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # station change from council:
        # old: Little Paxton Village Hall, Little Paxton, PE19 6EY
        # new: St James’ Church, High Street, Little Paxton, PE19 6NF
        if record.polling_place_id == "8945":
            record = record._replace(
                polling_place_name="St James’ Church",
                polling_place_address_1="High Street",
                polling_place_address_2="Little Paxton",
                polling_place_postcode="PE19 6NF",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.addressline6 in [
            # split
            "PE19 1HW",
            "PE28 2QG",
            "PE27 6DT",
            # suspect
            "PE29 1NY",
            "PE28 4NS",
            "PE28 4EW",
        ]:
            return None

        return super().address_record_to_dict(record)
