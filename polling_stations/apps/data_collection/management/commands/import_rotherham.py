from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000018"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019rother.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019rother.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000579433",  # S651LY -> S651NA : The Flat Eastwood View W.M.C., Fitzwilliam Road, Rotherham, South Yorkshire
            "10093477895",  # S648PG -> S648NA : Butchers Arms, Queen Street, Swinton, Mexborough, South Yorkshire
            "10000858047",  # S653LQ -> S653LG : The Flat Social Club, Laudsdale Road, Rotherham, South Yorkshire
            "100052107407",  # S652NW -> S652JY : 2 Barrett Corner, Rotherham, South Yorkshire
            "100052107408",  # S652NW -> S652JY : 3 Barrett Corner, Rotherham, South Yorkshire
            "100052107409",  # S652NW -> S652JY : 4 Barrett Corner, Rotherham, South Yorkshire
            "10091630096",  # S637LN -> S637LR : The Glasshouse, 41 Sandygate, Wath Upon Dearne, Rotherham, South Yorkshire
            "10091629451",  # S637DG -> S637DH : 11 Station Road, Wath Upon Dearne, Rotherham, South Yorkshire
            "10023208915",  # S648EG -> S648EF : Ring O`Bells, Church Street, Swinton, Mexborough, South Yorkshire
            "200000583027",  # S818BQ -> S818BA : Deep Carrs Farm, Lindrick Common, Worksop, Notts
            "100050870049",  # S651PQ -> S651PF : Cleveleys, 2 St Anns Road, Rotherham, South Yorkshire
            "10093479259",  # S652JY -> S652LD : 105A Chaucer Road, Rotherham, South Yorkshire
            "10093477892",  # S637HF -> S648RG : 20 Fitzwilliam Street, Wath Upon Dearne, Rotherham, South Yorkshire
            "10023213297",  # S636HF -> S636FH : 55 Roebuck Chase, Wath Upon Dearne, Rotherham, South Yorkshire
            "100052107406",  # S652NW -> S652JY : 1 Barrett Corner, Rotherham, South Yorkshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10023209193",  # S264TZ -> S263XJ : 12 Main Street, Swallownest, Sheffield, South Yorkshire
            "10023209192",  # S264TZ -> S263XJ : 10 Main Street, Swallownest, Sheffield, South Yorkshire
            "100052102914",  # S614DR -> S611HA : 125 Church Street, Rotherham, South Yorkshire
            "100052102913",  # S614DR -> S611HA : 123 Church Street, Rotherham, South Yorkshire
            "10032993851",  # S212DS -> S266NR : Lock Cottage Norwood Lock, Rotherham Road, Killamarsh, Sheffield, South Yorkshire
            "10032993852",  # S264UQ -> S266NR : 18 Queens Road, Swallownest, Sheffield, South Yorkshire
        ]:
            rec["accept_suggestion"] = False

        return rec
