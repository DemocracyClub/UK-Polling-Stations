from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IPS"
    addresses_name = (
        "2026-05-07/2026-02-26T10:30:43.578981/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-26T10:30:43.578981/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091059987",  # 22 LINGFIELD ROAD, IPSWICH
            "100091074230",  # 74 STRATFORD ROAD, IPSWICH
            "100091040532",  # 34 BROCKLEY CRESCENT, IPSWICH
            "10093557759",  # FLAT, THE INKERMAN PUBLIC HOUSE, 197 NORWICH ROAD, IPSWICH
            "100091060586",  # 1 LUTHER ROAD, IPSWICH
            "10035060422",  # THE STATION HOTEL, BURRELL ROAD, IPSWICH
            "100091045024",  # 41 COLERIDGE ROAD, IPSWICH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # station change from council:
        # OLD: Station Hotel, Burrell Road, Ipswich
        # NEW: Ground Floor Unit – Grafton House, 15-17 Russell Road, Ipswich, IP1 2DE
        if record.polling_place_id == "9770":
            record = record._replace(
                polling_place_name="Ground Floor Unit – Grafton House",
                polling_place_address_1="15-17 Russell Road",
                polling_place_postcode="IP1 2DE",
                polling_place_uprn="10003880936",
            )
        # Sikh Temple, Guru Nanak Gurdwara, 719 Bramford Road, Ipswich, IP1 5BD
        if record.polling_place_id == "9708":
            record = record._replace(
                polling_place_easting="613488",
                polling_place_northing="245784",
            )

        # Castle Hill United Reformed Church, Dryden Road, Ipswich, IP1 6QF
        if record.polling_place_id == "9762":
            record = record._replace(
                polling_place_easting="615235",
                polling_place_northing="247231",
            )

        # Stoke Green Baptist Church Hall, Halifax Road, Ipswich, IP2 8RE
        if record.polling_place_id == "9808":
            record = record._replace(
                polling_place_easting="615857",
                polling_place_northing="242747",
            )

        # Ascension Hall, Larchcroft Road, Ipswich, IP1 6AN
        if record.polling_place_id == "9738":
            record = record._replace(
                polling_place_easting="615625",
                polling_place_northing="246829",
            )

        # Broomhill Library, Sherrington Road, Ipswich, IP1 4HT
        if record.polling_place_id == "9734":
            record = record._replace(
                polling_place_easting="615423",
                polling_place_northing="245891",
            )

        # Belstead Arms Public House, Radcliffe Drive, Ipswich, IP2 9QA
        if record.polling_place_id == "9647":
            record = record._replace(
                polling_place_easting="613819",
                polling_place_northing="242425",
            )

        return super().station_record_to_dict(record)
