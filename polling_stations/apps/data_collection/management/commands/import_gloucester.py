from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000081'
    districts_name = 'City_of_Gloucester_New_Electoral_Sub_Districts'
    stations_name = 'New_City_of_Gloucester_Polling_Stations.shp'
    elections = ['local.gloucestershire.2017-05-04']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1],
            'name': "%s - %s" % (record[0], record[1]),
            'polling_station_id': record[1]
        }

    def station_record_to_dict(self, record):

        """
        This file had several data quality problems:

        01. Code QSV2 appeared twice with 2 polling stations:
            'Quedgeley Community Centre' and 'Meadowside School'
        02. Missing stations for districts 'QFC4' and 'B4'

        Joe queried with council and received reply:
        > The polling station for QSV2 is Meadowside Schol
        > The polling station for QFC4 is Quedgeley Community Centre
        > and for B4 it’s St. Lawrence Church Centre.

        Code includes manual bodges to deal with these cases.
        """

        if ',' in record[3]:
            codes = record[3].split(',')
        elif '-' in record[3]:
            codes = []
            if record[3][0:2] == "KW":
                codes = ['KW1', 'KW2', 'KW3', 'KW4']
            if record[3][0:3] == "QSV":
                # deliberately exclude QSV2 + sub in QFC4
                codes = ['QFC4', 'QSV3', 'QSV4']
        else:
            codes = [record[3]]

        # manually insert missing code B4
        if record[3].strip() == 'B2':
            codes.append('B4')

        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code.strip(),
                'postcode'           : '',
                'address'            : "\n".join([
                    str(record[1]).strip(),
                    str(record[2]).strip()
                ])
            })
        return stations
