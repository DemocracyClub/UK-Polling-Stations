from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000179"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy Club Data South Oxfordshire.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy Club Data South Oxfordshire.tsv"
    )
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # 3x station changes for EU Parl elections
        if record.polling_place_id == "6458":
            record = record._replace(polling_place_name="Benson Youth Hall")
            record = record._replace(polling_place_address_1="Oxford Road")
            record = record._replace(polling_place_address_2="Benson")
            record = record._replace(polling_place_address_3="Wallingford")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="OX10 6LX")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        if record.polling_place_id == "6775":
            record = record._replace(polling_place_name="Stoke Row Village Hall")
            record = record._replace(polling_place_address_1="Main Street")
            record = record._replace(polling_place_address_2="Stoke Row")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="RG9 5QL")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        if record.polling_place_id == "6491":
            record = record._replace(polling_place_name="St Catherine’s Church")
            record = record._replace(polling_place_address_1="Church Lane")
            record = record._replace(polling_place_address_2="Towersey")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="OX9 3QL")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        # 10090812631 assigned to polling station 6782. Rest of postcode assigned to 6607.
        # 10033011944 assigned to polling station 6765. Rest of postcode assigned to 6739.
        if record.post_code in ["RG8 9EY", "OX49 5BZ"]:
            return None

        return rec
