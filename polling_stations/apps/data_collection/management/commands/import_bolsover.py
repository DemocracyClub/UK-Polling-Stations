from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000033"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019bols.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019bols.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "3723":
            # Bolsover Parish Rooms, Hornscroft Road, Bolsover, Chesterfield
            record = record._replace(polling_place_postcode="S44 6HG")
        if record.polling_place_id == "3756":
            # The Shoulder at Hardstoft, Hardstoft, Chesterfield, Derbyshire
            record = record._replace(polling_place_postcode="S45 8AX")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 == "S80 ANL":
            record = record._replace(addressline6="S80 4NL")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013064940",  # wrong postcode in data and AddressBase
        ]:
            return None

        if uprn in [
            "200004517434",  # NG209RE -> NG209RF : Rectory Lodge, Rectory Road, Upper Langwith, Mansfield
            "10013069899",  # DE555AZ -> DE555TA : 28 Peregrine Way, Tibshelf, Alfreton, Derbyshire
        ]:
            rec["accept_suggestion"] = False

        return rec
