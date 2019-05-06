from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000117"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019burn.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019burn.CSV"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "100012382699":
            rec["postcode"] = "BB10 3QS"

        if uprn in [
            "10014136930",  # BB103PF -> BB103PQ : Swinden School House, Todmorden Road, Briercliffe, Burnley
            "10003781759",  # BB128EH -> BB128HD : 6 Smithy`s Court, Padiham, Burnley
            "10003781760",  # BB128EH -> BB128HD : 7 Smithy`s Court, Padiham, Burnley
            "100012383004",  # BB113EX -> BB113HB : Woodman Inn, Oxford Road, Burnley
            "100012382405",  # BB114NS -> BB114PG : Coal Clough Hotel, 41 Coal Clough Lane, Burnley
            "100012382408",  # BB114NW -> BB114NJ : Coal Clough Cottage, Coal Clough Lane, Burnley
            "10003758680",  # BB111JZ -> BB111JG : Inn On The Wharf, Manchester Road, Burnley
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012536092",  # BB102JF -> BB101XH : 5 Burnley Road, Briercliffe, Burnley
            "100012536996",  # BB112QR -> BB112RQ : Whinn Scarr, Moseley Road, Habergham Eaves, Burnley
            "100012537257",  # BB115NZ -> BB113ES : Springfield House, Clowbridge, Burnley
            "10003759507",  # BB127LA -> BB128HF : 11 Church Street, Hapton, Burnley
            "200001589427",  # BB115SA -> BB128TX : 1 Mere Court, Burnley
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "3683":
            record = record._replace(polling_place_postcode="BB11 3HL")

        if record.polling_place_id == "3656":
            record = record._replace(polling_place_postcode="BB11 5LZ")

        if record.polling_place_id == "3664":
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.292241, 53.790222, srid=4326)
            return rec

        return super().station_record_to_dict(record)
