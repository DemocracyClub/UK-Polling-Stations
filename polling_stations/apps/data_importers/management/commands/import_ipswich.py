from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IPS"
    addresses_name = (
        "2024-07-04/2024-05-28T16:02:04.832403/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T16:02:04.832403/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091059987",  # 22 LINGFIELD ROAD, IPSWICH
            "100091074230",  # 74 STRATFORD ROAD, IPSWICH
            "100091040532",  # 34 BROCKLEY CRESCENT, IPSWICH
            "10093557759",  # FLAT, THE INKERMAN PUBLIC HOUSE, 197 NORWICH ROAD, IPSWICH
        ]:
            return None

        if record.addressline6 in [
            "IP1 6GF",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Sikh Temple, Guru Nanak Gurdwara, 719 Bramford Road, Ipswich, IP1 5BD
        if record.polling_place_id == "8762":
            record = record._replace(
                polling_place_easting="613488",
                polling_place_northing="245784",
            )

        # Castle Hill United Reformed Church, Dryden Road, Ipswich, IP1 6QF
        if record.polling_place_id == "8744":
            record = record._replace(
                polling_place_easting="615235",
                polling_place_northing="247231",
            )

        # Stoke Green Baptist Church Hall, Halifax Road, Ipswich, IP2 8RE
        if record.polling_place_id == "8988":
            record = record._replace(
                polling_place_easting="615857",
                polling_place_northing="242747",
            )

        # Ascension Hall, Larchcroft Road, Ipswich, IP1 6AN
        if record.polling_place_id == "8772":
            record = record._replace(
                polling_place_easting="615625",
                polling_place_northing="246829",
            )

        # Broomhill Library, Sherrington Road, Ipswich, IP1 4HT
        if record.polling_place_id == "8776":
            record = record._replace(
                polling_place_easting="615423",
                polling_place_northing="245891",
            )

        # Belstead Arms Public House, Radcliffe Drive, Ipswich, IP2 9QA
        if record.polling_place_id in [
            "8968",
            "9076",
        ]:
            record = record._replace(
                polling_place_postcode="IP2 9QU",
                polling_place_easting="613819",
                polling_place_northing="242425",
            )

        return super().station_record_to_dict(record)
