from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000102"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May20193r.tsv"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May20193r.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"

    def station_record_to_dict(self, record):
        # station change for EU Parl elections
        if record.polling_place_id == "3643":
            record = record._replace(
                polling_place_name="Mill End Community Centre Hall"
            )
            record = record._replace(polling_place_address_1="Church Lane")
            record = record._replace(polling_place_address_2="Mill End")
            record = record._replace(polling_place_address_3="Rickmansworth")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="WD3 8HE")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090789736":
            rec["postcode"] = "WD5 0GF"
        if uprn in [
            "100081289658",  # WD35LW -> WD35LL : Viewpoint, Old Common Road, Chorleywood, Rickmansworth, Hertfordshire
            "200000943009",  # WD35NL -> WD33AN : 3A New Parade, Chorleywood, Rickmansworth, Hertfordshire
        ]:
            rec["accept_suggestion"] = False

        return rec
