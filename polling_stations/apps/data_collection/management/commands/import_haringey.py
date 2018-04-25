import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from pollingstations.models import PollingStation

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000014'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Haringey.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Haringey.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    station_id_field = 'polling_place_district_reference'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10022938046':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N4 1JZ'
            return rec

        if record.addressline6 == 'N8 8JP' and record.addressline2 == '8 Hornsey Park Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N8 0JP'
            return rec

        if record.addressline6 == 'N22 5JH' and record.addressline2 == '176 Mount Pleasant Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N17 6JQ'
            return rec

        if uprn == '10003982605':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N22 5AD'
            return rec

        if record.addressline6 == 'N15 5DJ' and record.addressline2 == '45A Broad Lane':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N15 4DJ'
            return rec

        if record.addressline6 == 'N17 6PF' and record.addressline2 == '36 Downhills Park Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N17 6PD'
            return rec

        return super().address_record_to_dict(record)

    # Haringey have supplied an additional file with
    # better grid references for the polling stations
    def post_import(self):
        filepath = os.path.join(
            self.base_folder_path,
            'local.2018-05-03/Version 2/Polling_Stations_2018-eastings-and-northings Haringey.csv'
        )
        self.csv_delimiter = ','
        gridrefs = self.get_data('csv', filepath)

        print("Updating grid refs...")
        for record in gridrefs:
            district_id = record.districts.strip()
            stations = PollingStation.objects.filter(
                council_id=self.council_id,
                internal_council_id=district_id
            )
            if len(stations) == 1:
                station = stations[0]
                station.location = Point(
                    float(record.east),
                    float(record.north),
                    srid=27700
                )
                self.check_station_point({
                    'location': station.location,
                    'council_id': station.council_id,
                })
                station.save()
            else:
                print("Could not find station id " + district_id)
        print("...done")
