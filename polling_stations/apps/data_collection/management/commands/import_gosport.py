from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000088'
    addresses_name = 'local.2018-05-03/Version 2/2018 LGE - Borouh of Gosport Democracy_Club__03May2018 v2.TSV'
    stations_name = 'local.2018-05-03/Version 2/2018 LGE - Borouh of Gosport Democracy_Club__03May2018 v2.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'PO12 2BY':
            return None

        return super().address_record_to_dict(record)
