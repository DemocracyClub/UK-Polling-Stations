from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = (
        "2022-05-05/2022-03-16T15:16:10.701979/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-16T15:16:10.701979/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Walter G Pomeroy Hall, Royal Lane, Hillingdon
        if record.polling_place_id == "11594":
            record = record._replace(polling_place_easting="506536")
            record = record._replace(polling_place_northing="181610")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        # Correction from Council
        if uprn in [
            "10095322450",
            "10095322452",
            "10095322453",
            "100021454152",
            "100021454154",
            "100021454156",
            "100021454217",
            "100021454218",
            "100021454148",
        ]:
            rec = super().address_record_to_dict(record)
            rec["polling_station_id"] = "11638"
            return rec

        if uprn in [
            "100022832219",
            "100021461989",
        ]:
            return None

        if record.addressline6 in [
            "UB8 3DG",
            "HA4 0SE",
            "UB10 0QB",
            "UB3 2FH",
            "UB3 3FN",
            "UB3 3PF",
            "UB7 9GA",
            "UB8 3DH",
            "UB8 3FE",
            "UB8 3QD",
            "UB8 3QT",
        ]:
            return None

        return super().address_record_to_dict(record)
