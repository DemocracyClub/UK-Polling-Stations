from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id      = 'E07000117'
    addresses_name  = 'parl.2017-06-08/Version 3/Burnley-Democracy_Club__08June2017resend.CSV'
    stations_name   = 'parl.2017-06-08/Version 3/Burnley-Democracy_Club__08June2017resend.CSV'
    elections       = ['parl.2017-06-08']
