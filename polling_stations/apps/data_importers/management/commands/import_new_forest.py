from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NEW"
    addresses_name = (
        "2023-05-04/2023-03-06T10:28:37.564607/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-06T10:28:37.564607/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # corrections from council
        if (
            record.polling_place_id == "8713"
        ):  # Fritham Free Church -> Bramshaw Village Hall
            record = record._replace(
                polling_place_name="Bramshaw Village Hall",
                polling_place_address_1="Bramshaw",
                polling_place_address_4="Lyndhurst",
                polling_place_postcode="SO43 7JE",
                polling_place_easting="426868",
                polling_place_northing="115670",
            )

        if (
            record.polling_place_id == "8818"
        ):  # Fordingbridge Town Hall, 63 High Street, Fordingbridge, SP6 1AS
            record = record._replace(polling_place_easting="414713")
            record = record._replace(polling_place_northing="114134")
        if (
            record.polling_place_id == "8963"
        ):  # Totton & Eling Cricket Club, Southern Gardens, Ringwood Road, Totton, Southampton, SO40 8RW
            record = record._replace(polling_place_easting="435298")
            record = record._replace(polling_place_northing="113155")

        # Hordle Pavilion, Vaggs Lane, Hordle, Lymington, SO41 0FP
        # correction for the council
        if record.polling_place_id == "8890":
            record = record._replace(polling_place_easting="426635")
            record = record._replace(polling_place_northing="95901")

        # The Glen, Butts Ash Lane, Hythe, Southampton, SO45 3RF
        # correction for the council
        if record.polling_place_id == "8859":
            record = record._replace(polling_place_easting="441940")
            record = record._replace(polling_place_northing="105830")

        # Fawley Royal British Legion, 3 Exbury Road, Blackfield, Southampton, SO45 1XD
        # correction for the council
        if record.polling_place_id == "8810":
            record = record._replace(polling_place_easting="444266")
            record = record._replace(polling_place_northing="102155")

        # Ibsley Village Hall, Gorley Road, Mockbeggar, Ringwood, BH24 3NL
        # correction for the council
        if record.polling_place_id == "8923":
            record = record._replace(polling_place_easting="416222")
            record = record._replace(polling_place_northing="109818")

        # Beaulieu Road Hotel, Beaulieu Road, Beaulieu, Brockenhurst, SO42 7YQ
        # correction for the council
        if record.polling_place_id == "8759":
            record = record._replace(polling_place_easting="435052")
            record = record._replace(polling_place_northing="106236")

        # River Of Life Church, The Life Centre Hall, Wootton Road, Tiptoe, Lymington, SO41 6FT
        # correction for the council
        if record.polling_place_id == "8894":
            record = record._replace(polling_place_easting="425768")
            record = record._replace(polling_place_northing="97540")

        # Bashley Village Hall, Bashley Road, Bashley, BH25 5RY
        # correction for the council
        if record.polling_place_id == "8696":
            record = record._replace(polling_place_easting="424231")
            record = record._replace(polling_place_northing=" 97058")

        # QE2 Recreation Centre, Thornbury Avenue, Blackfield, Southampton, SO45 1YP
        # correction for the council
        if record.polling_place_id == "8814":
            record = record._replace(polling_place_easting="444613")
            record = record._replace(polling_place_northing="101761")

        # Milford Village Hall, 2 Park Road, Milford on Sea, Lymington, SO41 0QU
        # correction for the council
        if record.polling_place_id == "8901":
            record = record._replace(polling_place_easting="429151")
            record = record._replace(polling_place_northing="91871")

        # Lymington Sea Scouts Hall, King`s Saltern Road, Lymington, SO41 3QD
        # correction for the council
        if record.polling_place_id == "8873":
            record = record._replace(polling_place_easting="433199")
            record = record._replace(polling_place_northing="94700")

        # Lyndhurst Community Centre, Car Park, Off High Street, Lyndhurst, SO43 7NY
        # correction for the council
        if record.polling_place_id == "8876":
            record = record._replace(polling_place_easting="429927")
            record = record._replace(polling_place_northing="108113")

        # , St George`s Centre, Tristan Close, Calshot, Southampton, SO45 1BN
        # correction for the council
        if record.polling_place_id == "8802":
            record = record._replace(polling_place_easting="447616")
            record = record._replace(polling_place_northing="101494")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013640427",  # ACORNS 47 BELMORE LANE, LYMINGTON, SO41 3NR
        ]:
            return None

        return super().address_record_to_dict(record)
