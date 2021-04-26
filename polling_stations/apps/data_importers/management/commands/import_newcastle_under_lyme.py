from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEC"
    addresses_name = (
        "2021-04-16T12:45:06.761928/Newcastle under lyme Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-04-16T12:45:06.761928/Newcastle under lyme Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Higherland Methodist Church Hall Higherland Newcastle Staffs ST5 2TF
        if record.polling_place_id == "1927":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032219337",  # ARDENNE THE AVENUE, KIDSGROVE
            "10024255961",  # 4B WARWICK CLOSE, KIDSGROVE, STOKE-ON-TRENT
            "10024255960",  # 4A WARWICK CLOSE, KIDSGROVE, STOKE-ON-TRENT
            "200004607891",  # STORE 3 LAWSON TERRACE, PORTHILL, NEWCASTLE UNDER LYME
            "10002238202",  # 3 LAWSON TERRACE, NEWCASTLE
            "200002872601",  # 125A LIVERPOOL ROAD, NEWCASTLE
            "100031730123",  # 79 KNUTTON LANE, NEWCASTLE UNDER LYME
            "100031730122",  # 77 KNUTTON LANE, NEWCASTLE UNDER LYME
            "200001160997",  # SUITE 2 HANOVER COURT HANOVER STREET, NEWCASTLE UNDER LYME
            "200004616065",  # 2 EARDLEYEND ROAD, NEWCASTLE UNDER LYME
            "200004617440",  # 93-94 LEYCETT LANE, LEYCETT, NEWCASTLE UNDER LYME
            "200004602621",  # AUSTIN LEYCETT LANE, SILVERDALE, NEWCASTLE UNDER LYME
            "10002237282",  # WILLOUGHBRIDGE WELLS LODGE, WILLOUGHBRIDGE, MARKET DRAYTON
            "200004612280",  # CARAVAN RED STREET STABLES TALKE ROAD, BRADWELL, NEWCASTLE UNDER LYME
        ]:
            return None

        if record.addressline6 in [
            "ST7 1DY",
            "ST5 8DS",
            "ST5 3ES",
            "ST5 7ES",
            "ST5 2TP",
            "ST5 2HN",
            "ST5 2PU",
            "ST5 1AU",
            "ST5 4DU",
            "TF9 4EY",
            "ST7 1LH",
            "ST5 1HN",
            "ST5 6AL",
        ]:
            return None

        return super().address_record_to_dict(record)
