from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000225"
    addresses_name = "parl.maybe/Version 1/chichester-Democracy_Club__15October2019.tsv"
    stations_name = "parl.maybe/Version 1/chichester-Democracy_Club__15October2019.tsv"
    elections = ["parl.maybe"]
    csv_delimiter = "\t"

    def get_station_point(self, record):
        return None

    def station_record_to_dict(self, record):

        # Rake Village Hall
        if record.polling_place_id == "2978":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002469481",  # GU273PT -> GU273PS : Fern Owls, Marley Common, Haslemere
            "10002471049",  # GU273HG -> GU273HQ : Verdley Hill House, Henley Hill, Henley, Haslemere
            "10002471776",  # GU290DL -> GU290DH : The Rectory, Heyshott, Midhurst
            "10002469418",  # GU273NG -> GU273NE : The Old School, Linchmere, Haslemere
            "10002474152",  # PO180QA -> PO180QB : 2 Parks Cottages, Goodwood, Chichester
            "10002474153",  # PO180QA -> PO180QB : 3 Parks Cottages, Goodwood, Chichester
            "10002470466",  # RH201JP -> RH201JH : Sorrells Cottage, Fittleworth, Pulborough
            "10002468852",  # RH201EZ -> RH201PZ : Redhill Hollow, Coates, Fittleworth, Pulborough
            "10002467828",  # GU289LY -> GU289LX : Palfrey Farmhouse, London Road, Petworth
            "200001740904",  # GU299QT -> GU299QJ : Pitsham Place, Pitsham, Midhurst
            "10002466508",  # GU84TA -> GU84SX : The Lodge, Shillinglee, Chiddingfold, Godalming
            "100061750085",  # PO188QG -> PO188RQ : Fairview, Priors Leaze Lane, Hambrook, Chichester
            "100062185216",  # PO188QG -> PO188RQ : Fairsend (Winter Quarters), Priors Leaze Lane, Hambrook, Chichester
            "200002892282",  # PO188QG -> PO188RQ : Hower Place (Winter Quarters), Priors Leaze Lane, Hambrook, Chichester
            "10002473175",  # PO207BZ -> PO207DA : Rideau Cottage, Shipton Green, Itchenor, Chichester
            "100061736996",  # PO208EB -> PO208AA : Buckleberries, 11 Cakeham Road, West Wittering, Chichester
            "10008886679",  # PO197BB -> PO197JR : Suite 848, 26 The Hornet, Chichester
            "10002467582",  # GU289LJ -> GU289NE : Freehold Farmhouse, Northchapel, Petworth
            "10002466676",  # GU290BU -> GU290BX : 123 Ambersham Moor, Selham Road, Ambersham, Midhurst
            "10002482519",  # GU315BU -> GU315EB : The Log Cabin Fyning Hill, Rogate, Petersfield
            "10093117146",  # PO108FW -> PO108HG : 10 Brewery Close, Southbourne, Emsworth
            "10093117147",  # PO108FW -> PO108HG : 11 Brewery Close, Southbourne, Emsworth
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10014108090",  # GU273NQ -> GU273NG : Rose Cottage Linchmere Marsh, Linchmere, Haslemere
            "100062416341",  # PO209DR -> PO209EL : 10 Granada, Selsey Country Club, Golf Links Lane, Selsey, Chichester
            "100062416343",  # PO209DR -> PO209EL : 12 Granada, Selsey Country Club, Golf Links Lane, Selsey, Chichester
            "100062186194",  # PO197QL -> PO197HN : Over the Way, Westhampnett Road, Chichester
        ]:
            rec["accept_suggestion"] = False

        return rec
