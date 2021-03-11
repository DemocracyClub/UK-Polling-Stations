from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STE"
    addresses_name = "2021-03-10T15:09:53.140416/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-10T15:09:53.140416/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3455144295",  # 2A EGERTON ROAD, HARTSHILL, STOKE-ON-TRENT
            "3455154988",  # RAILWAY COTTAGE, WEDGWOOD DRIVE, BARLASTON, STOKE-ON-TRENT
            "3455121928",  # BYCARS HOUSE, BYCARS ROAD, STOKE-ON-TRENT
            "3455043112",  # 184 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455091787",  # 2A HEATHCOTE ROAD, STOKE-ON-TRENT
            "3455091783",  # 3 SPRING GARDEN ROAD, STOKE-ON-TRENT
            "3455091782",  # 188 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455091781",  # 198 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455091779",  # 190 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455091778",  # 182 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455144033",  # 3 GRAVELLY BANK, STOKE-ON-TRENT
            "3455112142",  # 1 GRAVELLY BANK, STOKE-ON-TRENT
            "3455040966",  # 192 STAR & GARTER ROAD, STOKE-ON-TRENT
            "3455144383",  # 28A COBRIDGE ROAD, STOKE-ON-TRENT
            "3455154307",  # HOLLY LODGE RESIDENTIAL HOME, GASKELL ROAD, STOKE-ON-TRENT
            "3455130597",  # 3 BETHESDA MEWS, BETHESDA STREET, STOKE-ON-TRENT
            "3455017354",  # FLAT ABOVE 59 LICHFIELD STREET, HANLEY, STOKE-ON-TRENT
            "3455122809",  # FLAT FIRST FLOOR 342 HARTSHILL ROAD, HARTSHILL, STOKE-ON-TRENT
        ]:
            return None

        if record.addressline6 in [
            "ST4 2LE",
            "ST3 5HU",
            "ST3 4DH",
            "ST3 4HU",
            "ST3 7RX",
            "ST4 8NU",
            "ST3 7HQ",
            "ST3 5BN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Boothen Neighbourhood Centre Summer Street Off London Road Boothen Stoke-on-Trent ST4 4DW
        if record.polling_place_id == "14371":
            record = record._replace(polling_place_postcode="ST4 4DH")

        # Penkhull Village Hall Trent Valley Road Penkhull Stoke-on-Trent ST4 7LG
        if record.polling_place_id == "14352":
            record = record._replace(polling_place_postcode="ST4 5JB")

        # Civic Centre Glebe Street Stoke-on-Trent ST4 6RG
        if record.polling_place_id == "14342":
            record = record._replace(polling_place_postcode="ST4 1HH")

        # Park Evangelical Church Boughey Road Shelton Stoke-on-Trent ST4 2EB
        if record.polling_place_id == "14317":
            record = record._replace(polling_place_postcode="ST4 2BZ")

        # St John`s Community Church Baptist Street Burslem Stoke-on-Trent
        if record.polling_place_id == "14434":
            record = record._replace(polling_place_postcode="ST6 3BS")

        return super().station_record_to_dict(record)
