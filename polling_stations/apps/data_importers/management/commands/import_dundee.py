from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DND"
    addresses_name = "2026-06-18/2026-05-28T11:17:37.670858/Democracy Club - Idox_2026-05-28 11-14.csv"
    stations_name = "2026-06-18/2026-05-28T11:17:37.670858/Democracy Club - Idox_2026-05-28 11-14.csv"
    elections = ["2026-06-18"]

    # ignore the warnings for the following stations, council has confirmed postcodes:
    # Foula Terrace Sheltered, Housing Communal Lounge, Foula Terrace, Dundee, DD4 9SS
    # St Margaret's Church Hall, 1 Guthrie Terrace, Broughty Ferry, Dundee, DD5 2QY

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                # "117080095",  # LOWNIE HILL COTTAGE, FORFAR
                # "117087696",  # WOODSIDE, NETHER TULLOES FARM, FORFAR
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "DD4 0FD",
            "DD4 9ET",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # maintaing corrections through a by-election
        # # add missing postcode for: Glamis Heritage Education Centre, Glamis
        # if record.pollingstationnumber == "80":
        #     record = record._replace(pollingstationpostcode="DD8 1RS")

        # # add missing postcode for: Kingoldrum Village Hall, Kingoldrum
        # if record.pollingstationnumber == "70":
        #     record = record._replace(pollingstationpostcode="DD8 5HW")

        return super().station_record_to_dict(record)
