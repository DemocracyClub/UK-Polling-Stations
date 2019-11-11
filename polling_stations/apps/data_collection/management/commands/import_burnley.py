from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000117"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019burn.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019burn.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

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
            "10003759507",  # BB127LA -> BB128HF : 11 Church Street, Hapton, Burnley
            "200001589427",  # BB115SA -> BB128TX : 1 Mere Court, Burnley
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4502":
            record = record._replace(polling_place_postcode="BB10 4SN")

        if record.polling_place_id == "4447":
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.292241, 53.790222, srid=4326)
            return rec

        return super().station_record_to_dict(record)
