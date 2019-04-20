import os
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000045"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.CSV"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def pre_import(self):
        gridrefs_file = os.path.join(
            self.base_folder_path, "local.2019-05-02/Version 1/grid_refs.csv"
        )
        gridrefs = self.get_data("csv", gridrefs_file)
        self.gridrefs = {
            row.polling_station_id: {"easting": row.easting, "northing": row.northing}
            for row in gridrefs
        }

    def station_record_to_dict(self, record):
        polling_place_id = record.polling_place_id
        record = record._replace(
            polling_place_easting=self.gridrefs[polling_place_id]["easting"]
        )
        record = record._replace(
            polling_place_northing=self.gridrefs[polling_place_id]["northing"]
        )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # most of these UPRNs are junk
        if uprn.endswith("000000"):
            rec["uprn"] = ""

        if record.addressline6.strip() == "TQ13 8JG":
            rec["postcode"] = "TQ13 9JG"

        if (
            record.addressline1.strip() == "Little Park Farm"
            and record.addressline2.strip() == "Doddiscombsleigh"
            and record.addressline3.strip() == "Exeter"
            and record.addressline6.strip() == "EX6 8PA"
        ):
            rec["postcode"] = "EX6 7PZ"

        if (
            record.addressline1.strip() == "Flat 3 Old Globe Hotel"
            and record.addressline2.strip() == "15 North Street"
            and record.addressline3.strip() == "Ashburton"
            and record.addressline6.strip() == "TQ13 9HD"
        ):
            rec["postcode"] = "TQ13 7QH"

        if uprn in [
            "10032970638",  # TQ121BX -> TQ121BU : Ground Floor, 48 Keyberry Road, Newton Abbot
            "10032971784",  # EX70LX -> EX70DE : Flat 2, 3 Oak Park Villas, Dawlish
            "10032955461",  # TQ139TR -> TQ139SN : Wray Farm, Moretonhampstead Road, Lustleigh, Newton Abbot
            "10032973091",  # TQ148EG -> TQ148EA : Flat Above, 48 Teign Street, Teignmouth
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10032977482",  # TQ122FX -> TQ139RT : 34 Orleigh Cross, Newton Abbot
            "10032967238",  # EX29UH -> EX67DD : 2 The Court, Dunchideock, Exeter
            "10032976388",  # EX67LQ -> EX67XZ : Coombehead Farm, Pound Lane, Bridford, Exeter
            "10032970470",  # TQ148TG -> TQ148TJ : Eastleigh Cottage, First Drive, Dawlish Road, Teignmouth
        ]:
            rec["accept_suggestion"] = False

        return rec
