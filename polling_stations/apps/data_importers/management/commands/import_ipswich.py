from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IPS"
    addresses_name = (
        "2023-05-04/2023-04-13T10:22:11.453698/Democracy_Club__04May2023.tsv"
    )

    stations_name = (
        "2023-05-04/2023-04-13T10:22:11.453698/Democracy_Club__04May2023.tsv"
    )

    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091059987",  # 22 LINGFIELD ROAD, IPSWICH
            "100091074230",  # 74 STRATFORD ROAD, IPSWICH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Sikh Temple, Guru Nanak Gurdwara, 719 Bramford Road, Ipswich, IP1 5BD
        if record.polling_place_id == "8287":
            record = record._replace(
                polling_place_easting="613488",
                polling_place_northing="245784",
            )

        # Castle Hill United Reformed Church, Dryden Road, Ipswich, IP1 6QF
        if record.polling_place_id == "8272":
            record = record._replace(
                polling_place_easting="615235",
                polling_place_northing="247231",
            )

        # Stoke Green Baptist Church Hall, Halifax Road, Ipswich, IP2 8RE
        if record.polling_place_id == "8316":
            record = record._replace(
                polling_place_easting="615857",
                polling_place_northing="242747",
            )

        # Ascension Hall, Larchcroft Road, Ipswich, IP1 6AN
        if record.polling_place_id == "8207":
            record = record._replace(
                polling_place_easting="615625",
                polling_place_northing="246829",
            )

        # Broomhill Library, Sherrington Road, Ipswich, IP1 4HT
        if record.polling_place_id == "8211":
            record = record._replace(
                polling_place_easting="615423",
                polling_place_northing="245891",
            )

        # Belstead Arms Public House, Radcliffe Drive, Ipswich, IP2 9QA
        if record.polling_place_id == "8072":
            record = record._replace(
                polling_place_postcode="IP2 9QU",
                polling_place_easting="613819",
                polling_place_northing="242425",
            )

        return super().station_record_to_dict(record)
