from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E08000003"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019MAN.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019MAN.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "WA15 8XL":
            return None

        if record.addressline6.strip() == "M15 4PF":
            rec["postcode"] = "M15 4PS"
            return rec

        # Incorrect postcode for property
        if record.property_urn.strip().lstrip("0") == "10094426675":
            rec["postcode"] = "M40 1LU"

        # Incorrect postcode for property corrected from ab and checked against onspd
        if (
            "Williams Court" in record.addressline1
            and "Hope Road" in record.addressline2
        ):
            rec["postcode"] = "M14 5EU"

        # invalid postcodes
        if record.addressline6.strip() == "M13 OFN":
            rec["postcode"] = "M13 0FN"

        if record.addressline6.strip() == "M11 IJJ":
            rec["postcode"] = "M11 1JJ"

        if record.addressline6.strip() == "M22 OJA":
            rec["postcode"] = "M22 0JA"

        return rec
