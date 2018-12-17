import os
from django.core.exceptions import ObjectDoesNotExist
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from pollingstations.models import PollingStation
from uk_geo_utils.geocoders import AddressBaseGeocoder, AddressBaseException


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000029'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Solihull.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Solihull.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'CV7 7SQ':
            return None

        if uprn == '10090945566':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B94 6BD'
            return rec

        if uprn in ['10090946240', '10090946268']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B93 8NA'
            return rec

        if uprn in ['10008211727', '10008211728']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B91 2JJ'
            return rec

        if record.addressline6 == 'CV7 7HN':
            return None

        if record.addressline6 == 'CV7 7HL':
            return None

        return super().address_record_to_dict(record)

    # Solihull have supplied an additional file with
    # UPRNs for the polling stations
    def post_import(self):
        filepath = os.path.join(
            self.base_folder_path,
            'local.2018-05-03/Version 2 - UPRN/uprns.csv'
        )
        self.csv_delimiter = ','
        uprns = self.get_data('csv', filepath)

        print("Updating UPRNs...")
        for record in uprns:
            stations = PollingStation.objects.filter(
                council_id=self.council_id,
                internal_council_id=record.polling_place_id
            )
            if len(stations) == 1:
                station = stations[0]

                try:
                    uprn = record.uprn.lstrip('0')
                    g = AddressBaseGeocoder(record.polling_place_postcode)
                    location = g.get_point(uprn)
                except (ObjectDoesNotExist, AddressBaseException):
                    location = None
                station.location = location

                self.check_station_point({
                    'location': station.location,
                    'council_id': station.council_id,
                })
                station.save()
            else:
                print("Could not find station id " + self.get_station_hash(record))
        print("...done")
