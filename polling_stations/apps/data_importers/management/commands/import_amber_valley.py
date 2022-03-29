from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = "2022-05-05/2022-03-22T09:50:28.814111/Polling Districts 2022.csv"
    stations_name = "2022-05-05/2022-03-22T09:50:28.814111/Polling Stations 2022.csv"
    elections = ["2022-05-05"]

    # Not all wards are up for election this year. Hence 40,880 of ~64k
    # addresses are mapped. Have checked that mapped areas align with ward
    # boundaries. For details of which wards have elections, see
    # https://www.ambervalley.gov.uk/councillors-and-elections/elections/5-may-2022/.
