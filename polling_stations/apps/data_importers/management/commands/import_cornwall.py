from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CON"
    addresses_name = "2021-04-13T12:17:52.148354/cornwall-deduped.tsv"
    stations_name = "2021-04-13T12:17:52.148354/cornwall-deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Amendments from previous elections:

        # Methodist Sunday School Room Canworthy Water Launceston PL15 8UW
        if record.polling_place_id == "10617":
            record = record._replace(polling_place_uprn="10003300470")

        # The Cove Hall Wilcove Torpoint PL11 2PT
        if record.polling_place_id == "10171":
            record = record._replace(polling_place_uprn="10003065058")
            record = record._replace(polling_place_postcode="PL11 2PQ")

        # St Austell Rugby Club Tregorrick Lane St Austell PL26 7FH
        if record.polling_place_id == "9840":
            record = record._replace(polling_place_uprn="10002694687")

        # Millbrook Village Hall The Parade Millbrook Torpoint
        if record.polling_place_id == "10307":
            record = record._replace(
                polling_place_uprn="10023432417", polling_place_postcode="PL10 1AX"
            )

        # Removing postcode which look incorrect:

        # Bangors Methodist Church Poundstock Bude EX23 0DG
        if record.polling_place_id == "10700":
            record = record._replace(polling_place_postcode="")

        # The Victory Hall St Francis Road Indian Queens St Columb TR9 6JR TR9 6JR
        if record.polling_place_id == "9889":
            record = record._replace(
                polling_place_postcode="", polling_place_address_4=""
            )

        # Truro Railway Inn Railway Station Station Road Truro TR1 3HH
        if record.polling_place_id == "10927":
            record = record._replace(polling_place_postcode="")

        # Making sure postcodes are the same for stations at same location:

        # Memorial Hall - Station 2 Dobwalls Liskeard PL14 6JE
        # set to same as Memorial Hall - Station 1 Dobwalls Liskeard PL14 6LS
        if record.polling_place_id == "10208":
            record = record._replace(polling_place_postcode="PL14 6LS")

        # Station 2 St Erme Village Hall St Erme Truro TR2
        # set to same as Station 1 St Erme Village Hall St Erme Truro TR4 9BJ
        if record.polling_place_id == "10783":
            record = record._replace(polling_place_postcode="TR4 9BJ")

        # Station 1 Memorial Hall Trencrom Lane Carbis Bay St Ives TR26 2TQ
        # set to same as Station 2 Memorial Hall Trencrom Lane Carbis Bay St Ives TR26 2TA
        if record.polling_place_id == "10439":
            record = record._replace(polling_place_postcode="TR26 2TA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000078530",  # TREGONGEEVES COTTAGE, ST. AUSTELL
            "10090521508",  # THE HOUSE, UNION HILL, TRURO
            "10090519509",  # MEADOW VIEW TREGADDRA FARM CURY CROSS LANES, HELSTON
            "10094078885",  # CARAVAN 5A GWINEAR DOWNS, LEEDSTOWN
            "10094078364",  # WHOMPING WILLOW, CROFT PASCOE, GOONHILLY DOWNS, HELSTON
            "10093250953",  # ACCOMMODATION CHERRYWOOD LODGE POLPERRO ROAD, WEST LOOE
        ]:
            return None

        if record.addressline6 in [
            "TR16 5DD",
            "TR16 5QD",
            "TR10 8DH",
            "PL26 6AS",
            "PL32 9UN",
            "PL15 7SE",
            "PL15 8RF",
            "PL15 7SL",
            "PL32 9PN",
            "TR18 5DG",
            "TR18 5NA",
            "TR19 7JR",
            "PL17 7GB",
            "PL14 3JY",
            "PL25 4EL",
            "PL30 3DH",
            "PL26 8TF",
            "PL12 6RA",
            "TR18 3NH",
            "TR26 1EZ",
            "PL18 9BJ",
            "TR27 4RZ",
            "TR19 6BH",
            "TR14 8TY",
            "PL11 2HW",
            "TR14 0FY",
            "PL31 2PB",
            "TR18 4JY",
            "TR27 4AG",
            "PL15 8BE",
            "PL12 4RL",
        ]:
            return None

        return super().address_record_to_dict(record)
