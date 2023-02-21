from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "VAL"
    addresses_name = "2021-03-18T11:03:17.493346/UPDATED Democracy_Club__06May2021.TSV"
    stations_name = "2021-03-18T11:03:17.493346/UPDATED Democracy_Club__06May2021.TSV"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        # discard records in South Oxfordshire
        if record.polling_place_district_reference.startswith(
            "L"
        ) or record.polling_place_district_reference.startswith("R"):
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10014028754",  # CHURCH PATH FARM, FARINGDON
            "10014025441",  # CROSS BARGAIN COTTAGE, KINGSTON LISLE, WANTAGE
            "10093199254",  # FLAT 2 12 BATH STREET, ABINGDON
            "10014070551",  # GINGE MANOR STABLES, GINGE, WANTAGE
            "10093199253",  # FLAT 1 12 BATH STREET, ABINGDON
        ]:
            return None

        if record.addressline6 in [
            "OX11 6DA",
            "OX11 6DG",
            "OX11 9NX",
            "OX13 5GW",
            "SN7 7SX",
            "OX11 6EQ",
            "SN7 8DJ",
            "OX14 5DL",
            "OX13 5PS",
            "OX14 4DS",
            "OX12 7FS",
            "OX13 5GL",
            "OX14 4BF",
            "SN7 8QH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # discard records in South Oxfordshire
        if record.polling_place_district_reference.startswith(
            "L"
        ) or record.polling_place_district_reference.startswith("R"):
            return None

        # Polling place grid ref wrong.
        if record.polling_place_id in ["8409"]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        # Church of The Holy Ascension Littleworth Faringdon
        if record.polling_place_id == "11738":
            record = record._replace(polling_place_easting="431246")
            record = record._replace(polling_place_northing="197151")
            record = record._replace(polling_place_postcode="SN7 8EF")

        # Radley Church Room Church Road Radley OX14 2JE
        if record.polling_place_id == "11228":
            record = record._replace(polling_place_easting="452231")
            record = record._replace(polling_place_northing="199390")
            record = record._replace(polling_place_postcode="OX14 3QF")

        return super().station_record_to_dict(record)
