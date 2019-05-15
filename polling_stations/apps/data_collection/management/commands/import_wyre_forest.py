from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000239"
    addresses_name = "local.2019-05-02/Version 2/Democracy Club (1).csv"
    stations_name = "local.2019-05-02/Version 2/Democracy Club (1).csv"
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

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
            "10003382039",  # DY122RE -> DY104ND : B14 Riverside Caravan Park, Greenacres Lane, Dowles Road, Bewdley, Worcestershire
            "10003379973",  # DY122QG -> DY149EB : Caravan T04, Hillcroft Caravan Park, Cleobury Road, Bewdley, Worcestershire
            "10003374954",  # DY103RT -> DY103PX : 56 Westley Court, Austcliffe Lane, Cookley, Kidderminster, Worcestershire        ]:
        ]:
            rec["accept_suggestion"] = False

        return rec
