from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000045"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019tein.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019tein.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Alice Cross Day Centre
        if record.polling_place_id == "7231":
            record = record._replace(polling_place_easting="293930")
            record = record._replace(polling_place_northing="73047")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

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

        if record.addressline6.strip() == "TQ12 1FB":
            return None

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
