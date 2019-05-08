from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000244"
    addresses_name = "local.2019-05-02/Version 1/EastSuffolkCouncil - PDs.csv"
    stations_name = "local.2019-05-02/Version 1/EastSuffolkCouncil - Stations.csv"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # St Philips Church
        # user issue report #112
        if record.stationcode == "181":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(1.335067, 51.962539, srid=4326)
            return rec

        # Village Hall Barsham
        # user issue report #118
        if record.stationcode == "8":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(1.522623, 52.450787, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013328792",  # NR347DQ -> NR347DJ : Pinetrees, Park Drive, Beccles
            "10012981034",  # NR349TU -> NR349PU : 8 St Andrews Road, Beccles
            "10013331693",  # NR351BZ -> NR351BY : The Annexe, 67 Lower Olland Street, Bungay
            "10012979638",  # IP200PN -> IP200PR : Greenside Farm, The Green, South Elmham St Margaret, Harleston
            "10012979623",  # IP200PN -> IP200PR : Holly Tree Cottage, The Green, South Elmham St Margaret, Harleston
            "10012982450",  # NR348HZ -> NR348NF : Brook Farm, Halesworth Road, Redisham, Beccles
            "100091400931",  # NR348LR -> NR348LA : Corner Cottage, Cromwell Road, Ringsfield, Beccles
            "100091401913",  # NR348LY -> NR348LN : Dove Cottage, Redisham Road, Ringsfield, Beccles
            "10012977169",  # NR324WW -> NR324GF : 3 Townsend Way, Oulton, Lowestoft
            "10012977131",  # NR324WX -> NR324GD : 2 Dawson Mews, Oulton, Lowestoft
            "10012977132",  # NR324WX -> NR324GD : 4 Dawson Mews, Oulton, Lowestoft
            "10012977134",  # NR324WX -> NR324GD : 8 Dawson Mews, Oulton, Lowestoft
            "10012977135",  # NR324WX -> NR324GD : 10 Dawson Mews, Oulton, Lowestoft
            "10012977136",  # NR324WX -> NR324GD : 12 Dawson Mews, Oulton, Lowestoft
            "10013329842",  # NR348ET -> NR348ER : The Cartshed At Stoven Hall, Southwold Road, Stoven, Beccles
            "10012976656",  # NR322AN -> NR322AX : 1 Zanetta Court, Trafalgar Street, Lowestoft
            "100091406249",  # NR325PL -> NR325AU : Flowerlands, Flixton Road, Blundeston, Lowestoft
            "10012982806",  # NR325PQ -> NR325LB : Whitehouse Cottage, Rackhams Corner, Blundeston, Lowestoft
            "10012978467",  # NR325PQ -> NR325DG : Cul Na Feragh, Rackhams Corner, Corton, Lowestoft
            "10012979226",  # NR323BH -> NR323BW : 19 Hobart Way, Oulton, Lowestoft
            "10013326043",  # NR324UF -> NR324XJ : 11 Field Grange, Oulton, Lowestoft
            "10013326045",  # NR324UF -> NR324XJ : 17 Field Grange, Oulton, Lowestoft
            "100091408467",  # IP186SD -> IP186SB : Craigmyle House, St Felix School, Halesworth Road, Reydon, Southwold
            "10012979693",  # NR348BQ -> NR348BG : Cherry Tree Cottage, Clay Common Lane, Uggeshall, Beccles
            "100091394639",  # IP171QW -> IP171RY : Friston Lodge, Farnham Road, Snape, Saxmundham
            "100091392652",  # IP100AZ -> IP100BB : Dairy Farm, Brightwell Street, Brightwell, Ipswich
            "100091399513",  # IP122SY -> IP122JY : 2 White Cross Farm, Snape Road, Tunstall, Woodbridge
            "200004662747",  # IP123PG -> IP123PJ : 40 Fenn Row, Wantisden, Woodbridge
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013604974"  # IP124PQ -> IP121BW : Boat Ray, Martlesham Creek Boatyard, Church Lane, Martlesham, Woodbridge
        ]:
            rec["accept_suggestion"] = False

        return rec
