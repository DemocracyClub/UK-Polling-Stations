from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000015"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019derby.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019derby.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # user error report #202
        # Rebecca House, Uttoxeter Old Road
        if record.polling_place_id == "9315":
            record = record._replace(polling_place_easting="434237")
            record = record._replace(polling_place_northing="336464")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if (
            record.addressline1.strip() == "Flat 1"
            and record.addressline2.strip() == "48 Bedford Street"
            and record.addressline3.strip() == "Derby"
        ):
            rec["postcode"] = "DE22 3PB"

        if (
            record.addressline1.strip() == "43A Coronation Avenue"
            and record.addressline2.strip() == "Alvaston"
            and record.addressline3.strip() == "Derby"
        ):
            rec["postcode"] = "DE24 0LR"

        if uprn == "10010687582":
            rec["postcode"] = "DE22 4LT"

        if uprn in [
            "10010687003",  # DE236SX -> DE238SX : Flat c, 202 St Thomas` Road, Derby
            "200001878041",  # DE240LU -> DE248LU : Flat 2, 70 Wilkins Drive, Allenton, Derby
            "100030341735",  # DE248BH -> DE248BG : 40A Nightingale Road, Derby
            "10010683517",  # DE39GW -> DE39GB : Flat 1, 30 Poppyfields Drive, Mickleover, Derby
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100032256980",  # DE11RZ -> DE11RY : 112 Green Lane, Derby
            "100030362297",  # DE231HD -> DE231LH : 420A Stenson Road, Sunnyhill, Derby
            "10010685239",  # DE240UQ -> DE248UQ : The Needles, Bembridge Drive, Alvaston, Derby
            "100030323067",  # DE221GZ -> DE231DG : 20 Highfield Road, Derby
            "100030301767",  # DE39FT -> DE236WG : 20 Chestnut Avenue, Mickleover, Derby
            "10071154563",  # DE13GB -> DE13DZ : Flat Above The Flowerpot, 23 King Street, Derby
            "10010673524",  # DE222DL -> DE221BG : Flat Above, 508 Duffield Road, Allestree, Derby
            "100030342785",  # DE217GZ -> DE216AN : 211 Nottingham Road, Spondon, Derby
            "10010678922",  # DE221JH -> DE11EP : 10 St George`s Close, Allestree, Derby
            "100030297262",  # DE248DT -> DE238RT : Ground Floor Flat, 90 Marlborough Road, Derby
            "100030360196",  # DE248QG -> DE238QX : First Floor, 1162 London Road, Alvaston, Derby
            "10071156845",  # DE13AZ -> DE236BJ : 3B North Street, Derby
        ]:
            rec["accept_suggestion"] = False

        return rec
