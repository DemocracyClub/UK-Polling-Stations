from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E08000003"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 Manchester.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 Manchester.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding postcode
        """
        if record.polling_place_id == "5720":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

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

        return rec
