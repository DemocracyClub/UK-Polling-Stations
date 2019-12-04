from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000239"
    addresses_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019WF.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019WF.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        if record.addressline6 == "DY10 3JM":
            record = record._replace(addressline6="DY10 3JH")

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100120753042":
            rec["accept_suggestion"] = False  # incorrect 100% match "correction"

        if uprn in [
            "100120751152",  # DY122BL -> DY122LQ : Grove Farm, Dry Mill Lane, Bewdley, Worcestershire
            "10003375008",  # DY122PE -> DY122RE : B7A, Riverside Caravan Park, Greenacres Lane, Dowles Road, Bewdley
            "200001890773",  # DY122TN -> DY122TP : Dorbett Cottage, Leight Lane, Bewdley, Worcestershire
            "100120751024",  # DY122QE -> DY122PG : High Bank, Cleobury Road, Bewdley, Worcestershire
            "10003368650",  # DY115QT -> DY102EW : 6 Horsefair, Kidderminster, Worcestershire
            "100120753177",  # DY115QT -> DY102EW : 2ND Floor Flat, 9 Horsefair, Kidderminster, Worcestershire
            "100120751825",  # DY121QD -> DY138PX : New Barns Cottage, Blackstone, Bewdley, Worcs
            "10003371091",  # DY104PE -> DY104PF : Sion House Cottage, Hill Pool, Chaddesley Corbett, Kidderminster, Worcestershire
            "10003369782",  # DY102QD -> DY104QH : Copperfields, Holloway Road, Chaddesley Corbett, Kidderminster, Worcestershire
            "200001851612",  # DY102QD -> DY104QH : Holloway Farm, Holloway Road, Chaddesley Corbett, Kidderminster, Worcestershire
            "10003370000",  # DY115XR -> DY115XD : Pipers Croft, Wolverley Village, Kidderminster, Worcestershire
            "100121394380",  # DY103NR -> DY103NN : Railway Cottage, Birmingham Road Kidderminster, Worcestershire
            "100121394379",  # DY104NB -> DY103NN : Little Dunclent Farm Barn, Deansford Lane, Blakedown, Kidderminster, Worcs
            "10003368265",  # DY103NN -> DY104ND : 1 Bissell Cottage, Deansford Lane, Harvington, Kidderminster, Worcs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100120738036",  # DY101PX -> DY101PS : Flat 4 Compton Valley House, 90 George Street, Kidderminster, Worcestershire
        ]:
            rec["accept_suggestion"] = False

        return rec
