from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000005"
    addresses_name = "local.2018-05-03/Version 1/DC.TSV"
    stations_name = "local.2018-05-03/Version 1/DC.TSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "2162":
            record = record._replace(polling_place_postcode="OL12 7JG")

        if record.polling_place_id == "1958":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.property_urn.strip() == "23108461":
            return None

        if record.property_urn.strip() == "23081457":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OL12 9AA"
            return rec

        if record.addressline6 == "OL16 3BX":
            return None

        if record.property_urn.strip() == "10023364627":
            rec = super().address_record_to_dict(record)
            rec["polling_station_id"] = ""
            return rec

        if record.addressline6 == "OL16 4RF":
            return None

        if record.addressline6 == "OL12 8DW":
            return None

        if record.property_urn.strip() == "10090921994":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OL12 7RF"
            return rec

        if record.addressline6 == "OL12 8TN":
            return None

        if record.property_urn.strip() == "23099282":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "OL11 3AU"
            return rec

        if record.addressline6 == "OL16 1FD":
            return None

        if record.addressline6 == "M24 2SA":
            return None

        if record.addressline6 == "OL12 9BA":
            return None

        if record.property_urn.strip() == "10023364816":
            return None

        if record.addressline6 == "OL16 5SJ":
            return None

        return super().address_record_to_dict(record)
