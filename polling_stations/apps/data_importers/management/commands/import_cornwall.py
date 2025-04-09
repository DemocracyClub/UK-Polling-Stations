from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CON"
    addresses_name = (
        "2025-05-01/2025-03-26T14:41:05.807414/Democracy_Club__01May2025 1.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T14:41:05.807414/Democracy_Club__01May2025 1.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Amendment from previous election:
        # Millbrook Village Hall The Parade Millbrook Torpoint
        if record.polling_place_id == "18055":
            record = record._replace(polling_place_uprn="10023432417")

        # Station coords from council for:
        # Trevenson Church Community Hall, Church Road, Pool, Redruth, TR15 3PT
        if record.polling_place_id == "18651":
            record = record._replace(
                polling_place_easting="166658",
                polling_place_northing="41812",
                polling_place_uprn="10013623443",
            )

        # East Taphouse Community Hall, Salts Meadow Road, East Taphouse, Liskeard, PL14 4TG
        if record.polling_place_id == "18556":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
                polling_place_uprn="010003070931",
            )

        # St Breward Village Hall. Churchtown, Wet Lane, St Breward, Bodmin, PL30 4PP
        if record.polling_place_id == "19071":
            record = record._replace(
                polling_place_easting="209731",
                polling_place_northing="77253",
                polling_place_uprn="10003295304",
            )

        # Troon Church Hall, Treslothan Road, Troon, Camborne TR14 9EJ
        if record.polling_place_id == "18479":
            record = record._replace(
                polling_place_easting="165957",
                polling_place_northing="37924",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100040012372",  # REDCLIFFE HOUSE, ST. MARTINS ROAD, LOOE
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX23 9FQ",
            "PL15 7BJ",
            "PL11 2HW",
            "TR27 4RZ",
            "TR8 4NR",
            "TR18 3NH",
            "TR16 5QD",
            "TR27 4AG",
            "TR20 8TG",
            "TR11 4PT",
            "PL18 9BJ",
            "PL30 3DH",
            "PL25 4EL",
            "TR10 9LJ",
            "PL31 2PB",
            "PL11 3DA",
            "TR2 5JS",
            "TR18 3NA",
            "PL32 9UN",
            "TR18 5NA",
            "PL15 8RF",
            "PL15 7SE",
        ]:
            return None
        return super().address_record_to_dict(record)
