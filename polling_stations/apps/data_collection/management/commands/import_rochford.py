from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000075"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Rochford.TSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Rochford.TSV"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "4117":
            record = record._replace(polling_place_postcode="SS6 7JP")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100090572258",  # SS54QE -> SS54PT : 15A Hockley Rise, Hawkwell, Hockley, Essex
            "200000266895",  # SS43JE -> SS43JD : Riverview, The Chase, Ashingdon, Rochford, Essex
            "10014205416",  # SS56ND -> SS56NB : 29 Tyndale House, Tyndale Close, Hullbridge, Hockley, Essex
            "100091596497",  # SS41AD -> SS41AB : 42/44 North Street, Rochford, Essex
            "10010565888",  # SS41AD -> SS41FJ : 1 Ethan Court, North Street, Rochford, Essex
            "10010565889",  # SS41AD -> SS41FJ : 2 Ethan Court, North Street, Rochford, Essex
            "10010565890",  # SS41AD -> SS41FJ : 3 Ethan Court, North Street, Rochford, Essex
            "10010565891",  # SS41AD -> SS41FJ : 4 Ethan Court, North Street, Rochford, Essex
            "100091263321",  # SS41NH -> SS41RA : 42 St Luke`s Place, Dalys Road, Rochford, Essex
            "100090595397",  # SS30LQ -> SS30GB : 342 Little Wakering Road, Barling Magna, Essex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10010562426"  # SS30GB -> SS30LA : 344A Little Wakering Road, Barling Magna, Essex
        ]:
            rec["accept_suggestion"] = False

        return rec
