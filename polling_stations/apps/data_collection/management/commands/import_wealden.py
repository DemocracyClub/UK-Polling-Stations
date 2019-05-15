from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000065"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wealdon.tsv"
    )
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wealdon.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033399978",  # TN224DB -> TN224BY : Stable Cottage, Uckfield Road, Herons Ghyll, Uckfield, East Sussex
            "10070937340",  # TN210BA -> TN210BD : Ghyll Park Farm, Little London Road, Heathfield, East Sussex
            "10033404720",  # TN210AY -> TN210BA : Little London House, Little London Road, Heathfield, East Sussex
            "10033414534",  # TN223DR -> TN223DN : Lampool Corner Cottage, Lampool Corner, Maresfield, Uckfield, East Sussex
            "10033414541",  # TN222EE -> TN222ED : Powdermill House, Maresfield, Uckfield, East Sussex
            "100062592501",  # TN74DA -> TN74DB : Summerford Cottage, Beech Green Lane, Withyham, East Sussex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100062557927",  # BN86HE -> TN225NR : Old Post House, The Street, Chiddingly, Lewes, East Sussex
            "100060123569",  # RH177LS -> RH177JQ : Anderida, Stone Quarry Road, Chelwood Gate, Haywards Heath, West Sussex
            "10033406575",  # TN39HG -> TN39HA : Singlegate Lodge, Frant Road, Frant, Tunbridge Wells, East Sussex
            "10033408533",  # TN56PQ -> TN56PG : The Oasthouse, Mousehall, Tidebrook Road, Wadhurst, East Sussex
            "10033413710",  # RH193PG -> RH193PE : Dutton Homestall Lodge, Homestall Road, Ashurst Wood, East Grinstead, West Sussex
            "10033413711",  # RH193PG -> RH193PE : Wilkey Down, Homestall Road, Ashurst Wood, East Grinstead, West Sussex
            "10033409990",  # BN271SF -> BN271SE : Larksmoor, Rickney Lane, Hailsham, East Sussex
            "10070938384",  # TN74LB -> TN74LA : The Caravan, North Clays, Butcherfield Lane, Hartfield, East Sussex
            "10033399568",  # TN223AS -> TN223AE : Chile Pine, 51 Millwood Lane, Maresfield, Uckfield, East Sussex
            "10093175153",  # TN219QB -> TN219QA : Mobile Home Little Harness Farm, Cowbeech Road, Rushlake Green, Heathfield, East Sussex
        ]:
            rec["accept_suggestion"] = False

        return rec
