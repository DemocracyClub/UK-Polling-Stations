from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000034"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019kirklees.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019kirklees.CSV"
    elections = ["local.2019-05-02"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # station changes for EU election
        if record.polling_place_id == "7685":
            record = record._replace(
                polling_place_name="Temporary Polling Station, BBG Academy"
            )

        if record.polling_place_id == "8151":
            record = record._replace(polling_place_name="Battyeford J & I School")
            record = record._replace(polling_place_address_1="Nab Lane")
            record = record._replace(polling_place_address_2="Battyeford")
            record = record._replace(polling_place_address_3="Mirfield")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="")
            record = record._replace(polling_place_uprn="")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.706736, 53.681520, srid=4326)
            return rec

        # user issue report #80
        if record.polling_place_id == "7820":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.6100925, 53.5945822, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "83246005":
            rec["postcode"] = "HD2 1HA"
            rec["accept_suggestion"] = False

        if uprn in [
            "83099017",  # HD13UN -> BD195EY : Flat Above, 50 Westgate, Cleckheaton
            "200003798939",  # HD76DU -> HD75TU : Throstle Green Farm, Holt Head Road, Slaithwaite, Huddersfield
            "83151141",  # WF134JD -> WF134JA : 1 the Bungalows, Halifax Road, Dewsbury
            "83199907",  # WF134JD -> WF134JA : 2 the Bungalows, Halifax Road, Dewsbury
            "83121884",  # BD194JP -> BD194AU : The Coach House, 291C Oxford Road, Gomersal, Cleckheaton
            "83002159",  # HD75UZ -> HD75UU : Outbarn, Laund Road, Slaithwaite, Huddersfield
            "83003456",  # HD74NN -> HD75UU : Nab Farm, Highfield Road, Slaithwaite, Huddersfield
            "83007989",  # HD75PW -> HD75TR : Pioneer Farm Cottage, 2 Blackmoorfoot Road, Linthwaite, Huddersfield
            "83007957",  # HD75PW -> HD75TR : Pioneer Farm Cottage, 1 Blackmoorfoot Road, Linthwaite, Huddersfield
            "83186093",  # HD75TY -> HD75HL : Holt Farm, Varley Road, Slaithwaite, Huddersfield
            "83132478",  # HD89TU -> HD89TD : Butts Top Cottage, Westfield Lane, Emley Moor, Huddersfield
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "83199052"  # BD194AZ -> BD194BE : The Coach House Clough Mills, Dewsbury Road, Gomersal, Cleckheaton
        ]:
            rec["accept_suggestion"] = False

        if uprn == "83099017":
            return None
        if record.addressline6.strip() == "BD19 5EY":
            return None

        if record.addressline6.strip() in ["HD8 8SB", "HD5 0RN"]:
            return None

        return rec
