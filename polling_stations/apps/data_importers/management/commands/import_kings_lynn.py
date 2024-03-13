from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = (
        "2024-05-02/2024-03-13T08:58:12.052675/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T08:58:12.052675/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # King`s Lynn Town Football Club, The Walks, Tennyson Avenue, KING`S LYNN PE30 5PB
        if record.polling_place_id == "27162":
            record = record._replace(
                polling_place_easting="562582",
                polling_place_northing="319608",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000033946",  # 81B HIGH STREET, KING'S LYNN
            "10090917704",  # 199 STATION ROAD, WATLINGTON, KING'S LYNN
            "10013001170",  # WHITE DYKE BUNGALOW, BLACK DYKE ROAD, HOCKWOLD, THETFORD
        ]:
            return None
        if record.addressline6 in [
            # split
            "PE30 5BD",
            # look wrong
            "PE30 1JG",
        ]:
            return None

        return super().address_record_to_dict(record)
