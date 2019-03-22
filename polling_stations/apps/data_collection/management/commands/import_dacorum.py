from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000096"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019 dacorum.CSV"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019 dacorum.CSV"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        # All of the UPRN data from Mole Valley is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "HP3 OAN":
            rec["postcode"] = "HP3 0AN"

        return rec
