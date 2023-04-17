from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROC"
    addresses_name = (
        "2023-05-04/2023-04-17T15:07:22.505468/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T15:07:22.505468/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010561894",  # THE PADDOCKS, VANDERBILT AVENUE, RAYLEIGH
            "100090575372",  # 4 TYRELLS, HOCKLEY
            "100090592879",  # 157 STAMBRIDGE ROAD, ROCHFORD
            "100091264335",  # BARROW HALL FARMHOUSE BARROW HALL ROAD, LITTLE WAKERING
            "100090595184",  # 56 LITTLE WAKERING ROAD, GREAT WAKERING, SOUTHEND-ON-SEA
        ]:
            return None

        if record.addressline6 in [
            "SS3 0GF",
            "SS3 0LQ",
            "SS6 8DF",
            "SS3 0HH",
            "SS3 0GE",
            "SS5 6FF",  # HILTON CRESCENT, HULLBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wesley Room, Methodist Church Hall, Eastwood Road, Rayleigh, Essex
        # Fixing the warning, correction is safe
        if record.polling_place_id == "5723":
            record = record._replace(polling_place_postcode="SS6 7JP")

        # Grange Free Church, London Road, Rayleigh, Essex, SS6 9AY
        if record.polling_place_id == "5869":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
