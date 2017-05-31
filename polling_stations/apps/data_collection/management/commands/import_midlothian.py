from data_collection.management.commands import BaseScotlandSpatialHubImporter

class Command(BaseScotlandSpatialHubImporter):
    council_id = 'S12000019'
    council_name = 'Midlothian'
    elections = [
        'local.midlothian.2017-05-04',
        #'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        code = str(record[0]).strip()

        """
        MN4H is represented as a polygon which sits on top of MN4G
        (as opposed to being in an InnerRing inside MN4G).
        This means any point which is in MN4H is also in MN4G.
        Fortunately MN4H and MN4G share the same polling
        station, so in this case we can fix it by just not importing MN4G.
        If they didn't use the same polling station, this would be an issue.
        """
        if code == 'MN4H':
            return None

        return super().district_record_to_dict(record)
