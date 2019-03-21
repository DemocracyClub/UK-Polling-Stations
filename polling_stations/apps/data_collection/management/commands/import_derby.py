from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000015"
    addresses_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019derby.tsv"
    stations_name = "local.2019-05-02/Version 3/Democracy_Club__02May2019derby.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

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

        if (
            record.addressline1.strip() == "Flat 2"
            and record.addressline2.strip() == "70 Wilkins Drive"
            and record.addressline3.strip() == "Allenton"
            and record.addressline4.strip() == "Derby"
        ):
            rec["postcode"] = "DE24 8LU"

        if uprn == "10010687582":
            rec["postcode"] = "DE22 4LT"

        if record.addressline6.strip() == "DE23 6GH":
            return None

        if uprn in [
            "100032007602",  # DE223FZ -> DE223SZ : Basement Flat, Flat 1, Rear of 302 Abbey Street, Derby
            "100032008969",  # DE234AA -> DE236AD : International Hotel, 288-290 Burton Road, Derby
            "10010687003",  # DE236SX -> DE238SX : Flat c, 202 St Thomas` Road, Derby
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100032256980",  # DE11RZ -> DE11RY : 112 Green Lane, Derby
            "100030362297",  # DE231HD -> DE231LH : 420A Stenson Road, Sunnyhill, Derby
            "10010685239",  # DE240UQ -> DE248UQ : The Needles, Bembridge Drive, Alvaston, Derby
            "100030323067",  # DE221GZ -> DE231DG : 20 Highfield Road, Derby
            "100030301767",  # DE39FT -> DE236WG : 20 Chestnut Avenue, Mickleover, Derby
            "100030342785",  # DE217GZ -> DE216AN : 211 Nottingham Road, Spondon, Derby
            "10071154563",  # DE13GB -> DE13DZ : Flat Above The Flowerpot, 23 King Street, Derby
        ]:
            rec["accept_suggestion"] = False

        return rec
