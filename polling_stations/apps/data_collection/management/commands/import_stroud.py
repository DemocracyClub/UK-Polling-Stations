from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000082'
    addresses_name = 'democracy_club__04may2017 (4).csv'
    stations_name = 'democracy_club__04may2017 (4).csv'
    elections = ['local.gloucestershire.2017-05-04']
    csv_encoding = 'latin-1'
