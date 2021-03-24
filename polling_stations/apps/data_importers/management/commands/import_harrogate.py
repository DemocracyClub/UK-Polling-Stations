from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAG"
    addresses_name = (
        "2021-03-24T11:03:45.408151/Democracy_Club__06May2021 amendments.CSV"
    )
    stations_name = (
        "2021-03-24T11:03:45.408151/Democracy_Club__06May2021 amendments.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100050407904",  # GROVE HOUSE BUNGALOW, SKIPTON ROAD, HARROGATE
            "100050429604",  # HAWTHORNS, STUDLEY ROAD, RIPON
            "10093034565",  # OAK HOUSE PENNY POT LANE TO CENTRAL HOUSE FARM, HAMPSTHWAITE
        ]:
            return None

        if record.addressline6 in [
            "HG3 5QF",
            "HG3 3AT",
            "HG3 3JQ",
            "HG2 9LJ",
            "HG1 4JW",
            "HG2 9NW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # North Stainley Village Hall North Stainley Ripon
        if record.polling_place_id == "14714":
            record = record._replace(polling_place_postcode="HG4 3JT")

        # Samwaies Hall Main Street Wath Ripon HG4 5AT
        if record.polling_place_id == "14943":
            record = record._replace(polling_place_postcode="HG4 5ET")

        # Dishforth Village Hall Main Street Dishforth
        if record.polling_place_id == "14932":
            record = record._replace(polling_place_postcode="YO7 3JU")

        return super().station_record_to_dict(record)
