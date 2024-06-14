from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = (
        "2024-07-04/2024-06-14T15:39:39.081592/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:39:39.081592/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "12180637",  # ANNEXE 20 LOCARNO ROAD, GREENFORD
            "12147146",  # 35A PRIORY GARDENS, LONDON
            "12181729",  # FLAT 3 55 PARK AVENUE, PARK ROYAL
            "12181728",  # FLAT 2 55 PARK AVENUE, PARK ROYAL
            "12181730",  # FLAT 4 55 PARK AVENUE, PARK ROYAL
            "12181731",  # FLAT 5 55 PARK AVENUE, PARK ROYAL
        ]:
            return None

        if record.addressline6 in [
            "W4 5HL",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for West London University Sports Pavilion, (Home of Pitshanger Football Club), Argyle Road, W13 8EL
        if record.polling_place_id == "7785":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
