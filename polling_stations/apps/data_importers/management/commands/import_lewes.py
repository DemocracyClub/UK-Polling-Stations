from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2024-05-02/2024-04-09T16:18:14.963158/Eros_SQL_Output002.csv"
    stations_name = "2024-05-02/2024-04-09T16:18:14.963158/Eros_SQL_Output002.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # fixes from council:

        # SAINT PETER THE APOSTLE CHURCH HALL-THE CHAPEL ROOMS, BELGRAVE ROAD, SEAFORD BN25 4PE
        if (
            self.get_station_hash(record)
            == "34-saint-peter-the-apostle-church-hall-the-chapel-rooms"
        ):
            record = record._replace(pollingstationpostcode="BN25 2HE")

        # SOCIAL CENTRE, LEWES ROAD, NEWHAVEN BN9 9BL
        if self.get_station_hash(record) == "17-social-centre":
            record = record._replace(pollingstationpostcode="BN9 9RW")

        # THE TOWN HALL - BAXTER CORRIDOR, FISHER STREET ENTRANCE, LEWES BN7 2DE
        if self.get_station_hash(record) == "14-the-town-hall-baxter-corridor":
            record = record._replace(pollingstationpostcode="BN7 2DG")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033272374",  # 24A STEYNING AVENUE, PEACEHAVEN
            "200001466148",  # OLD WHEEL COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
            "100062487484",  # WOODS COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
        ]:
            return None

        return super().address_record_to_dict(record)
