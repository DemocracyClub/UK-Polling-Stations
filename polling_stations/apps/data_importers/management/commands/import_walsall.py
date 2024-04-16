from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLL"
    addresses_name = (
        "2024-05-02/2024-03-13T13:07:56.064490/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T13:07:56.064490/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # street name changes from council:

        # old: Community Centre on Dudley Fields, Central Drive/Sneyd Hall Road, Walsall, WS3 2NP
        # new: Community Centre on Dudley Fields, Sneyd Hall Road, Walsall, WS3 2NP
        if record.polling_place_id == "3253":
            record = record._replace(polling_place_address_1="Sneyd Hall Road")

        # old: Palfrey Junior School (former Community Centre) , Dale Street, Walsall, WS1 4AH
        # new: Palfrey Junior School (former Community Centre) , Entrance Milton Street, Walsall, WS1 4AH
        if record.polling_place_id == "3500":
            record = record._replace(polling_place_address_1="Entrance Milton Street")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071349802",  # 659A WALSALL ROAD, WEDNESBURY
            "100071109642",  # 124 GOUGH STREET, WILLENHALL
            "10090065467",  # 123A GOUGH STREET, WILLENHALL
            "10090065466",  # 123 GOUGH STREET, WILLENHALL
            "100071062219",  # 240 INGRAM ROAD, WALSALL
            "100071062221",  # 242 INGRAM ROAD, WALSALL
            "200003317397",  # CHRIST CHURCH RECTORY, BLAKENALL HEATH, WALSALL
            "10013664575",  # 52 MATTESLEY COURT, CRESSWELL CRESCENT, WALSALL
            "200003317043",  # 103 SNEYD LANE, ESSINGTON, WOLVERHAMPTON
            "200003317044",  # 105 SNEYD LANE, ESSINGTON, WOLVERHAMPTON
            "200003317045",  # 107 SNEYD LANE, ESSINGTON, WOLVERHAMPTON
            "200003317046",  # 109 SNEYD LANE, ESSINGTON, WOLVERHAMPTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WS3 2DX",
            # look wrong
            "WS10 7TG",
            "WS2 0HS",
            "WS3 4NX",
            "WS3 4NT",
        ]:
            return None

        return super().address_record_to_dict(record)
