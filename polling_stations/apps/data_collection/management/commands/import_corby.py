from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000150"
    addresses_name = "2020-02-24T12:11:32.913518/Democracy_Club__07May2020corby.tsv"
    stations_name = "2020-02-24T12:11:32.913518/Democracy_Club__07May2020corby.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032145646",  # NN171EG -> NN171EE : 73B Occupation Road, Corby, Northants
            "100032145771",  # NN172AE -> NN171AE : The Best Western, Rockingham Forest Hotel, Rockingham Road, Corby, Northants
            "10006865553",  # NN172HP -> NN173LH : Laundimer House, 1 Bear`s Lane, Weldon, Corby, Northants
        ]:
            rec["accept_suggestion"] = True
        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7230":
            record = record._replace(polling_place_easting="487843")
            record = record._replace(polling_place_northing="286921")

        return super().station_record_to_dict(record)
