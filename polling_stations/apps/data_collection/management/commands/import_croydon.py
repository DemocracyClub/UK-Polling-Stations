from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E09000008"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.tsv"

    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "11078":
            record = record._replace(polling_place_easting="536768")
            record = record._replace(polling_place_northing="162439")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10093756524":  # Flat 4 Boileau Court, 449A Purley Way, Croydon
            rec["postcode"] = "CR04RG"
            rec["accept_suggestion"] = False
        if uprn == "10093048086":  # Flat 14, 3 Church Road, Croydon
            rec["postcode"] = "CR01FP"
            rec["accept_suggestion"] = False
        if uprn == "10093050442":
            rec["postcode"] = "CR05HL"  # Flat 6 Coach House, Oaks Road, Croydon
            rec["accept_suggestion"] = False
        if record.post_code == "CR0 7Q":
            rec["postcode"] = "CR0 7QN"

        if record.addressline6 in [
            "CR0 7UR",
            "CR0 5SH",
            "CR0 5BA",
            "CR2 0SA",
            "CR8 4HE",
        ]:
            return None

        if uprn in [
            "100020571691",  # CR35QX -> CR35QS : Wentworth, Fox Lane, Caterham, Surrey
            "100020640357",  # SE255BQ -> SE255DF : 1 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640358",  # SE255BQ -> SE255DF : 2 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640359",  # SE255BQ -> SE255DF : 3 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640360",  # SE255BQ -> SE255DF : 4 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640361",  # SE255BQ -> SE255DF : 5 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640362",  # SE255BQ -> SE255DF : 6 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640363",  # SE255BQ -> SE255DF : 7 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640364",  # SE255BQ -> SE255DF : 8 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100020640365",  # SE255BQ -> SE255DF : 9 Argyll Court, 130 Birchanger Road, South Norwood, London
            "100023258863",  # SE254PL -> SE254PT : Ground Floor Flat, 134 Portland Road, South Norwood, London
            "100023259899",  # SE254UF -> SE254UN : 49 Portland Road, South Norwood, London
            "10014049899",  # SE254UF -> SE254UN : 49A Portland Road, South Norwood, London
            "10090380070",  # CR01HD -> CR01RA : Ground Floor, 18 St. Peter`s Road, Croydon
            "200001203840",  # CR35QX -> CR35QS : The Bungalow, The Fox Inn, Fox Lane, Caterham, Surrey
            "200001218459",  # CR78SB -> CR78SD : Rear Flat, 434 Whitehorse Road, Thornton Heath
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10000105571",  # SW164BZ -> SW164AN : 1396B London Road, Norbury, London
            "10001008215",  # CR85JE -> CR82DB : 18A Godstone Road, Kenley
            "100020607347",  # CR82PA -> CR02BD : 42 Lansdowne Road, Purley
            "100020607351",  # CR82PA -> CR02BD : 44 Lansdowne Road, Purley
            "100020607409",  # CR82PE -> CR02BF : 81 Lansdowne Road, Purley
            "100020607420",  # CR82PE -> CR02BN : 95 Lansdowne Road, Purley
            "100020664258",  # CR84DU -> CR82HF : 17 Callow Field, Purley
            "100022902871",  # CR82PD -> CR02BX : 5 Lansdowne Road, Purley
            "100022902872",  # CR82PA -> CR02BX : 2 Lansdowne Road, Purley
            "100022902929",  # CR82PD -> CR02BX : 17 Lansdowne Road, Purley
            "100022903052",  # CR82PA -> CR02BD : 46 Lansdowne Road, Purley
            "100022903053",  # CR82PD -> CR02BE : 45 Lansdowne Road, Purley
            "100022904030",  # CR82PA -> CR02BD : 12 Lansdowne Road, Purley
            "100022904031",  # CR82PA -> CR02BD : 22 Lansdowne Road, Purley
            "100023534232",  # CR51EB -> CR52NH : Flat rear of, 266-268 Coulsdon Road, Coulsdon
            "10014051126",  # CR52NL -> CR53BP : 1 Well Cottage, Fourth Drive, Coulsdon
            "200001186634",  # CR01NA -> CR01ND : 58 High Street, Croydon
            "200001205005",  # CR82PA -> CR02BD : 16 Lansdowne Road, Purley
            "200001207021",  # CR82PA -> CR02BD : 18 Lansdowne Road, Purley
            "10090380070",
        ]:
            rec["accept_suggestion"] = False

        return rec
