from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000177"
    addresses_name = (
        "local.2019-05-02/Version 1/Cherwell DC - Democracy_Club__02May2019.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Cherwell DC - Democracy_Club__02May2019.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        # Following updates based on last year's corrections
        if record.polling_place_id == "16765":
            record = record._replace(polling_place_easting="445258")
            record = record._replace(polling_place_northing="240545")

        if record.polling_place_id == "16855":
            record = record._replace(polling_place_easting="456935")
            record = record._replace(polling_place_northing="222867")

        if record.polling_place_id == "16931":
            record = record._replace(polling_place_easting="435614")
            record = record._replace(polling_place_northing="237845")

        if record.polling_place_id == "16894":
            record = record._replace(polling_place_easting="442908")
            record = record._replace(polling_place_northing="241900")

        if record.polling_place_id == "17014":
            record = record._replace(polling_place_easting="458727")
            record = record._replace(polling_place_northing="231062")

        if record.polling_place_id == "17062":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        if record.polling_place_id == "17074":
            record = record._replace(polling_place_easting="449488")
            record = record._replace(polling_place_northing="214376")

        # New Correction, fall back to postcode.
        if record.polling_place_id == "16949":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        # Confirmed with Council
        if record.polling_place_id == "17233":
            record = record._replace(polling_place_easting="451146")
            record = record._replace(polling_place_northing="225741")

        if record.polling_place_id == "16870":
            record = record._replace(polling_place_postcode="OX26 6AU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10011929697":
            rec["postcode"] = "OX156NF"

        if uprn == "10011912082":
            rec["postcode"] = "OX160EJ"

        if uprn == "10011880980":
            rec["postcode"] = "OX156LD"

        if uprn == "10011880370":
            rec["postcode"] = "OX263WU"

        if uprn == "010011900272":
            rec["postcode"] = "OX155HL"

        if record.post_code == "OX25 5QH":
            rec["postcode"] = "OX255QG"
            rec["accept_suggestion"] = False

        if uprn in [
            "10011890896",  # OX154HD -> OX154HE : Bungalow Caravan Site, Milton Road, Milton, Banbury, Oxon
            "10011908055",  # OX156JA -> OX156HQ : Yarnhill Farm Shennington Road, Shennington Road, Epwell, Banbury, Oxon
            "10011900681",  # OX277SG -> OX277SQ : Baynards House, Baynards Green, Ardley, Bicester, Oxon.
            "100120802758",  # OX53DJ -> OX53HJ : Bell House, Church Lane, Kirtlington, Kidlington, Oxon
            "10011904348",  # OX52FN -> OX52DH : 3B The Hampden Building, High Street, Kidlington, Oxon
            "10011890641",  # OX52DS -> OX52DR : 95A High Street, Kidlington, Oxon
            "10011888902",  # OX253QU -> OX253QQ : Brookside, Oxford Road, Weston-on-the-Green, Bicester, Oxon
            "100120774559",  # OX155BW -> OX155DT : 15 Wykham Lane, Bodicote, Banbury, Oxon
            "100121287468",  # OX154SB -> OX154DB : The Courtyard, Chapel Lane, Bodicote, Banbury, Oxon
            "100121289268",  # OX165ST -> OX165XT : 20 Ashby Court, Banbury, Oxon
            "10011887046",  # OX169AA -> OX169AB : Flat 1, 43 South Bar Street, Banbury
            "10011903344",  # OX169AA -> OX169AF : Flat 6 Ivy House, 23 South Bar Street, Banbury
            "10011903340",  # OX169AA -> OX169AF : Flat 2 Ivy House, 23 South Bar Street, Banbury
            "10011919892",  # OX263YD -> OX252AN : 7 Honeysuckle Close, Bicester, Oxon
            "100120776194",  # OX262ND -> OX265EA : 4 Blenheim Drive, Bicester, Oxon
            "10011891593",  # OX154LH -> OX154LQ : The Lodge, Wigginton, Banbury, Oxon
            "10011906091",  # OX252PA -> OX252SP : Faccenda Chicken, Lakeside House, Wendlebury Road, Bicester, Oxon
            "10011890369",  # OX278RG -> OX278RJ : 2 Glebe Farm Cottages, Fringford, Bicester, Oxon
        ]:
            rec["accept_suggestion"] = True
        if uprn in [
            "10011918555",  # OX52GH -> OX52LB : Apartment 1 Burberry House, Blenheim Road, Kidlington, Oxon
            "10011918556",  # OX52GH -> OX52LB : Apartment 2 Burberry House, Blenheim Road, Kidlington, Oxon
            "10011918557",  # OX52GH -> OX52LB : Apartment 4 Burberry House, Blenheim Road, Kidlington, Oxon
            "10011918559",  # OX52GH -> OX52LB : Apartment 5 Burberry House, Blenheim Road, Kidlington, Oxon
            "10011901312",  # OX162BN -> OX172BN : 4 Blacklocks Hill, Nethercote, Banbury, Oxon
        ]:
            rec["accept_suggestion"] = False

        return rec
