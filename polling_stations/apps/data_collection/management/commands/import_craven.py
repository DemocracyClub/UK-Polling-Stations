from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000163"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019craven.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019craven.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ("LS29 0EU", "LS29 0RQ", "LA2 8PR"):
            # Postcode centroid across council boundary
            return None

        if record.addressline6 == "BD20 8HO":
            record = record._replace(addressline6="BD20 8HL")

        if (record.addressline1, record.addressline2) == ("26 High Street", "Gargrave"):
            # Previously associated UPRN was for misaddressed-in-AddressBase-to-include-'Gargrave' 26 High Street in
            # Skipton proper.
            record = record._replace(property_urn="10007560825")

        rec = super().address_record_to_dict(record)

        if uprn in [
            "10007566505",  # BD235EL -> BD235AD : Badger Hill House, Station Road, Threshfield, Skipton
            "10007564535",  # BD236DA -> BD236BU : Rosemary Cottage, Main Street, Appletreewick, Skipton
            "10007564837",  # LA27DQ -> LA27DH : Bowker House Farm, Mewith Lane, Bentham, Lancaster
            "100052044713",  # LA63HJ -> LA27HL : Greta Villa, 22 Main Street, Ingleton, Carnforth
            "100050346180",  # BD209AZ -> BD207LD : 1 South View, Farnhill, Keighley
            "10007559698",  # BD249PH -> BD240EH : The Old Schoolhouse, Stainforth, Settle
        ]:
            rec["accept_suggestion"] = False

        return rec
