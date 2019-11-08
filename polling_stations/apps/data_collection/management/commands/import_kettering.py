from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000153"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019kett.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019kett.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4976":
            record = record._replace(polling_place_postcode="NN16 0HA")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.property_urn == "100032143386" and record.post_code == "NN16 0TG":
            record = record._replace(property_urn="100031067936")

        # Wrong post code (NN15 7HQ) and location in AddressBase
        if "Clifton House" in record.addressline1 and record.post_code == "NN15 7NQ":
            record = record._replace(property_urn="")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007875190",  # NN168FX -> NN168XF : New Managers Flat at Telford Lodge, Rothwell Road, Kettering
            "10007870548",  # NN141QE -> NN141QF : The Hay Barn, Glendon Road, Rothwell, Kettering
            "10007865717",  # NN155JL -> NN155JA : 4 Keating Close, Kettering
            "10094094192",  # NN146AB -> NN146AD : Flat, 1 -  5 High Street, Rothwell, Kettering
            "10007867846",  # NN146AD -> NN146BQ : The Old Greyhound, High Street, Rothwell, Kettering
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10007869324",  # NN156NJ -> NN156NF : 3 The Lodge, Wicksteed Park, Barton Road, Kettering
            # AddressBase postcodes look suss
            "100031049769",  # NN168NE -> NN169LP : Grnd Flr Flat, 128 Bath Road, Kettering
            "100031056422",  # NN142SW -> NN141RG : Gaultney Wood Farm, Pipewell Road, Rushton, Kettering
            # Wrong UPRN
            "100032048111",  # LE168LU -> LE168QX : Dale Farm, Waterloo Park, Great Oxendon
            "10007869003",  # NN141RP -> NN141QE : Keepers Cottage, Desborough Road, Rushton, Kettering
            # Probably wrong UPRN
            "100032048441",  # LE168LF -> LE168LE : Bridge House, 2 Desborough Road, Braybrooke, Market Harborough
            # Not sure
            "100031076102",  # NN142RS -> NN142RL : Flat 2, 60 Station Road, Desborough, Kettering
            "100031075819",  # NN168LL -> NN168XZ : Manager`s Flat, The Warren, Stamford Road, Kettering
            # Addresses quite different between AddressBase and import data
            "100032142306",  # LE168LJ -> NN142LN : Braybrooke Farm, Harborough Road, Braybrooke, Leics
            # Not an attested address
            "10007863199",  # LE168LP -> LE168LF : 3 Park Lane, Braybrooke, Market Harborough
        ]:
            rec["accept_suggestion"] = False

        return rec
