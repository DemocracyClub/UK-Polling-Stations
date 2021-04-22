from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = (
        "2021-04-16T12:59:18.049121/Re-submission - Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-04-16T12:59:18.049121/Re-submission - Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Kidlington Youth Football Club
        if record.polling_place_id == "23006":
            record = record._replace(
                polling_place_uprn="10011878924",
                polling_place_easting="",
                polling_place_northing="",
            )

        # Following updates based on last year's corrections

        # The Peoples Church, Horsefair, Banbury, Oxon
        if record.polling_place_id == "22810":
            record = record._replace(polling_place_easting="445258")
            record = record._replace(polling_place_northing="240545")

        # West Bicester Community Centre, Bowmont Square, Bicester, Oxon
        if record.polling_place_id == "22911":
            record = record._replace(polling_place_easting="456935")
            record = record._replace(polling_place_northing="222867")

        # Sibford Gower Village Hall
        if record.polling_place_id == "23154":
            record = record._replace(polling_place_easting="435614")
            record = record._replace(polling_place_northing="237845")

        # Drayton Village Hall
        if record.polling_place_id == "23186":
            record = record._replace(polling_place_easting="442908")
            record = record._replace(polling_place_northing="241900")

        # St Mary the Virgin Church, Cottisford, Brackley, Northants
        if record.polling_place_id == "23075":
            record = record._replace(polling_place_easting="458727")
            record = record._replace(polling_place_northing="231062")

        # The Church of St John the Baptist, Broadway, Kidlington, Oxon
        if record.polling_place_id == "22985":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        # Kidlington Baptist Church, High Street, Kidlington, Oxon
        if record.polling_place_id == "23012":
            record = record._replace(polling_place_easting="449488")
            record = record._replace(polling_place_northing="214376")

        # Confirmed with Council
        # Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "23115":
            record = record._replace(polling_place_easting="451146")
            record = record._replace(polling_place_northing="225741")

        # Pingle Field Pavilion, Pingle Field, Bicester
        if record.polling_place_id == "22904":
            record = record._replace(polling_place_postcode="OX26 6AU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "OX16 9JU",
            "OX16 9QF",
            "OX16 5AW",
            "OX16 2BN",
            "OX16 2AS",
            "OX26 3EB",
            "OX26 3EZ",
            "OX26 6BP",
            "OX5 3DJ",
            "OX25 3QU",
            "OX5 1LZ",
            "OX5 1AJ",
            "OX27 7AE",
        ]:
            return None  # split

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            # Group 1
            "10011909033",
            "10011917099",
            # Group 2
            "10011924957",
            "10011924949",
            "10011924948",
            "10011924947",
            "10011924946",
            # Group 3
            "10011927441",
            "10011927442",
            "10011927443",
            "10011927445",
            "10011927446",
            "10011927448",
            "10011931230",
            # Group 4
            "10011889761",
        ]:
            return None  # long distance; crosses another polling district

        return super().address_record_to_dict(record)
