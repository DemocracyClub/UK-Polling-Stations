from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id      = 'E07000117'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Burnley.CSV'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Burnley.CSV'
    elections       = ['local.2018-05-03']
