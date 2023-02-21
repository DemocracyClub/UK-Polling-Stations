from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IPS"
    addresses_name = (
        "2022-05-05/2022-02-23T11:56:29.039800/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-02-23T11:56:29.039800/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Sikh Temple, Guru Nanak Gurdwara
        if record.polling_place_id == "7914":
            record = record._replace(polling_place_uprn="10035058265")

        # Castle Hill United Reformed Church
        if record.polling_place_id == "7930":
            record = record._replace(polling_place_uprn="100091483837")

        # Stoke Green Baptist Church Hall
        if record.polling_place_id == "7741":
            record = record._replace(polling_place_uprn="10004567047")

        # Ascension Hall
        if record.polling_place_id == "7748":
            record = record._replace(polling_place_uprn="200001930783")

        # Broomhill Library
        if record.polling_place_id == "7752":
            record = record._replace(polling_place_uprn="10004565452")

        # St Mark`s RC Church Hall
        if record.polling_place_id == "7777":
            record = record._replace(polling_place_easting="614239")
            record = record._replace(polling_place_northing="243310")

        # Belstead Arms Public House
        if record.polling_place_id == "7843":
            record = record._replace(
                polling_place_uprn="10004566897", polling_place_postcode="IP2 9QU"
            )

        # All Hallows Church Hall
        if record.polling_place_id == "7755":
            record = record._replace(
                polling_place_uprn="10004564821", polling_place_postcode="IP3 0EN"
            )

        return super().station_record_to_dict(record)
