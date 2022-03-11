from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = "2022-05-05/2022-03-11T13:34:54.264817/Cherwell District Council - Democracy_Club__05May2022.tsv"
    stations_name = "2022-05-05/2022-03-11T13:34:54.264817/Cherwell District Council - Democracy_Club__05May2022.tsv"
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Kidlington Youth Football Club
        if record.polling_place_id == "24875":
            record = record._replace(
                polling_place_uprn="10011878924",
                polling_place_easting="",
                polling_place_northing="",
            )

        # West Bicester Community Centre, Bowmont Square, Bicester, Oxon
        if record.polling_place_id == "24693":
            record = record._replace(polling_place_easting="456935")
            record = record._replace(polling_place_northing="222867")

        # St Mary the Virgin Church, Cottisford, Brackley, Northants
        if record.polling_place_id == "24828":
            record = record._replace(polling_place_easting="458727")
            record = record._replace(polling_place_northing="231062")

        # Drayton Village Hall
        if record.polling_place_id == "24717":
            record = record._replace(polling_place_easting="442908")
            record = record._replace(polling_place_northing="241900")

        # Sibford Gower Village Hall
        if record.polling_place_id == "24751":
            record = record._replace(polling_place_easting="435614")
            record = record._replace(polling_place_northing="237845")

        # Kidlington Baptist Church, High Street, Kidlington, Oxon
        if record.polling_place_id == "24895":
            record = record._replace(polling_place_easting="449488")
            record = record._replace(polling_place_northing="214376")

        # The Church of St John the Baptist, Broadway, Kidlington, Oxon
        if record.polling_place_id == "24883":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        # Pingle Field Pavilion, Pingle Field, Bicester
        if record.polling_place_id == "24685":
            record = record._replace(polling_place_postcode="OX26 6AU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "OX16 5AW",
            "OX16 9QF",
            "OX25 5BH",
            "OX26 3EB",
            "OX26 3EZ",
            "OX26 6HB",
            "OX27 7AE",
            "OX5 1LZ",
        ]:
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10011889761",
            "100121291839",
            "10011906163",
        ]:
            return None

        return super().address_record_to_dict(record)
