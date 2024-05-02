from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WGN"
    addresses_name = "2024-05-02/2024-03-26T12:26:18.296702/wigan-stations.csv"
    stations_name = "2024-05-02/2024-03-26T12:26:18.296702/wigan-stations.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002861926",  # THE COTTAGE, SANDY LANE, HINDLEY, WIGAN
            "100012500668",  # DODHURST BROW FARM, SANDY LANE, HINDLEY, WIGAN
            "100011823007",  # 165 WIGAN ROAD, ASHTON-IN-MAKERFIELD, WIGAN
            "10095424360",  # 109 ANCHOR FIELD, LEIGH
            "10095424324",  # 73 ANCHOR FIELD, LEIGH
            "10095424371",  # 120 ANCHOR FIELD, LEIGH
        ]:
            return None

        if record.postcode in [
            # splits
            "WN7 4TF",
            "WN7 1QA",
            "WN7 2LS",
            # suspect
            "WN7 4GL",
            "WN7 4GQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Aidans Parish Centre, Highfield Grange Ave, Winstanley, Wigan, WN3 6EE
        if record.pollingplaceid == "9761":
            record = record._replace(
                pollingplaceeasting="355847", pollingplacenorthing="402852"
            )

        # Standish Community Centre, Moody Street, Off Church, Street Standish, WN6 0JY
        if record.pollingplaceid == "9906":
            record = record._replace(
                pollingplaceeasting="356374", pollingplacenorthing="410043"
            )
        # User bug report #634
        # Moving point closer to access road for:
        # The Community Centre Hope Carr Road, Siddow Common, Leigh WN7 3ET
        if record.pollingplaceid == "9664":
            record = record._replace(
                pollingplaceeasting="366257", pollingplacenorthing="399402"
            )

        # User feedback, removes map of:
        # Ince Independent Methodist Church, Keble Street - Stopford Street Entrance, Ince, Wigan
        rec = super().station_record_to_dict(record)
        if rec["internal_council_id"] == "10025":
            rec["location"] = None
            return rec
        return super().station_record_to_dict(record)
