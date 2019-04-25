from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000032"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wand.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wand.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "6891":
            record = record._replace(polling_place_postcode="SW15 6JY")
        if record.polling_place_id == "6947":
            record = record._replace(polling_place_postcode="SW12 9QH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "121036893":
            rec["postcode"] = "SW169NN"
            rec["accept_suggestion"] = False

        if uprn in [
            "121048817",  # SW129BE -> SW129BA : Flat 1, 189 Balham High Road, London
            "121048818",  # SW129BE -> SW129BA : Flat 2, 189 Balham High Road, London
            "121048819",  # SW129BE -> SW129BA : Flat 3, 189 Balham High Road, London
            "10070243531",  # SW170TQ -> SW170RN : Ground Floor, 71-77 Tooting High Street, London
            "100022613240",  # SW113BP -> SW113BS : 262A Battersea Park Road, London
            "100022613241",  # SW113BP -> SW113BS : 262B Battersea Park Road, London
            "100022678378",  # SW166RS -> SW166RT : 7 Burney House, Pendle Road, London
            "121028687",  # SW155PJ -> SW115PJ : 29 Lawrence Froebel College, Roehampton Lane, London
            "100022668375",  # SW111BL -> SW113GZ : 103A Mallinson Road, London
            "100022613599",  # SW111BL -> SW113GZ : 103C Mallinson Road, London
            "121026201",  # SW111BH -> SW113GX : First Floor Flat, 125 Mallinson Road, London
            "100023297408",  # SW111JA -> SW111LP : 238 Lavender Hill, London
            "10024086170",  # SW154JL -> SW154JD : Huntercombe Hospital, Holybourne Avenue, London
            "121049779",  # SW156TH -> SW152TH : 282A Upper Richmond Road, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10091501706",  # SW129RN -> SW181HG : 18B Fernlea Road, London
            "10008156178",  # SW177BB -> SW179BU : A302 A Block, Furzedown Education Site, Spalding Road, London
            "10091500114",  # SW116QT -> SW170AD : 36 Belleville Road, London
            "10091500113",  # SW116QT -> SW170AD : 34 Belleville Road, London
            "100023304793",  # SW111XJ -> SW116SA : 15 Webbs Road, London
            "100022691028",  # SW115EB -> SW115SG : 27 Sugden Road, London
            "121050680",  # SW112RF -> SW111SX : Ground Floor Flat, 61 St John`s Hill Grove, London
            "121050681",  # SW112RF -> SW111SX : First Floor Flat, 61 St John`s Hill Grove, London
            "10090498932",  # SW115NW -> SW153LG : Ground Floor Flat, 28 Rush Hill Road, London
            "10090498931",  # SW115NW -> SW153LG : Flat 2, 28 Rush Hill Road, London
            "100022619566",  # SW185BQ -> SW116HU : 61 Brookwood Road, London
            "121036331",  # SW166LY -> SW176AW : Flat 3A, 101A Mitcham Lane, London
            "10093416547",  # SW114ND -> SW179PU : Flat A, 146 Battersea Park Road, London
            "10093416548",  # SW114ND -> SW179PU : Flat B, 146 Battersea Park Road, London
            "10093416549",  # SW114ND -> SW179PU : Flat C, 146 Battersea Park Road, London
            "10008158731",  # SW128EG -> SW115SD : Ground Floor Flat 1, 9 Heslop Road, London
            "121051162",  # SW182QZ -> SW182QU : 43 East Hill, London
            "121051059",  # SW182SL -> SW111PA : Flat B, 50 North Side Wandsworth Common, London
            "10091503361",  # SW151SS -> SW152PA : 97B Putney High Street, London
            "100023323171",  # SW177BZ -> SW177DF : 65-81 Beechcroft Road, London
            "100022644699",  # SW177LN -> SW178DJ : 167 Fishponds Road, London
            "121052234",  # SW185HT -> SW181RU : 60A West Hill Road, London
        ]:
            rec["accept_suggestion"] = False

        return rec
