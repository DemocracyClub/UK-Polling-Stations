from data_importers.management.commands import Unknown


class Command(Unknown):
    council_id = "MAN"
    addresses_name = "2023-05-04/2023-03-23T16:29:47.358436/Polling_Place_Postcode_Lookup__04May2023.tsv"
    stations_name = "2023-05-04/2023-03-23T16:29:47.358436/Polling_Place_Postcode_Lookup__04May2023.tsv"
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
