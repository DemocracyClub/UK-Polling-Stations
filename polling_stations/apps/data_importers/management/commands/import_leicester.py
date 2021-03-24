from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "LCE"
    addresses_name = (
        "2021-03-19T11:45:34.451844/Democracy Club Polling Stations List 6 May 2021.csv"
    )
    stations_name = (
        "2021-03-19T11:45:34.451844/Democracy Club Polling Stations List 6 May 2021.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_2",
    ]
    station_address_fields = ["polling_place_name", "polling_place_address_1"]

    def station_record_to_dict(self, record):

        # Evington Community Centre Kedleston Road
        if record.polling_place_id == "8567":
            record = record._replace(
                polling_place_address_1="Entrance from Kedleston Road"
            )

        # Splitting polling station addresses up accordingly
        if record.polling_place_id in [
            "8459",  # Mobile Polling Station, The Linwood Centre
            "8582",  # Goodwood Bowling & Social Club, Entrances From Uppingham Rd & Crofters Dr
            "8509",  # Shree Shakti Mandir, Moira Street
        ]:
            line2, postcode = record.polling_place_address_2.split(",")
            record = record._replace(
                polling_place_address_2=line2, polling_place_postcode=postcode
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "2465131722",  # HUMBERSTONE FARM, THURMASTON LANE, LEICESTER
        ]:
            return None

        if record.addressline6 in ["LE1 7GT", "LE5 4GA"]:
            return None

        if (
            "Thurcaston House" in record.addressline1
            or "Thurcaston House" in record.addressline2
        ):
            return None

        return super().address_record_to_dict(record)
