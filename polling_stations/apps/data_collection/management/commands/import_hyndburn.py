import re

from data_collection.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000120"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019hynd.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019hynd.tsv"
    elections = ["parl.2019-12-12"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "824":
            record = record._replace(polling_place_postcode="BB5 5DH")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if re.search(r"\bWhalley Road\b", record.addressline1) or re.search(
            r"\bWhalley Road\b", record.addressline2
        ):
            # This road passes through Great Harwood and Clayton le Moors with duplicated house numbers.
            # The council have misrecorded UPRNs for a lot of these properties
            rec["accept_suggestion"] = False

        # More misrecorded UPRNs
        if record.post_code in [
            "BB5 4PP",  # Confusion between Stanhill [Road] and Stanhill Lane
            "BB5 4PS",  # Confusion between Stanhill [Road] and Stanhill Lane
            "BB5 3RU",  # Confusion between Hoyle Bottom and Hoyle Bottom Farm Cottages
            "BB5 0HD",  # Confusion between George Streets in Accrington and Oswaldtwistle
            "BB5 4BQ",  # Confusion between Queens Road West in Accrington and Church
            "BB5 3BB",  # Confusion between High Streets in Accrington and Oswaldtwistle
        ]:
            rec["accept_suggestion"] = False

        if uprn == "10070894060":
            # Looks assigned to the wrong polling place
            return None

        if uprn in [
            "10009970126",  # BB56EW -> BB56QT : Peel Park Hotel, Turkey Street, Accrington, Lancashire
            "10009971723",  # BB56EW -> BB56QT : Peel Park Cottage, Turkey Street, Accrington, Lancashire
            "100012544978",  # BB51EH -> BB51EN : 33 Abbey Street, Accrington, Lancashire
            "10070886537",  # BB56NT -> BB56PN : Flat Over, Hyndburn Private Clinic, Avenue Parade, Accrington
            "100012546116",  # BB55UT -> BB55UR : Waterside Bungalow, Altham, Accrington, Lancashire
            "100010451238",  # BB67QL -> BB67QQ : 19-21 Queen Street, Great Harwood, Blackburn, Lancashire
            "100010446019",  # BB67DF -> BB67DE : 45 Blackburn Road, Great Harwood, Blackburn, Lancashire
            "10009971276",  # BB55QA -> BB55PZ : Royal Oak Hotel, 35 Sparth Road, Clayton-Le-Moors, Accrington
            "100010446896",  # BB67NF -> BB67QB : 17 Church Street, Great Harwood, Blackburn, Lancashire
            "100012392089",  # BB54QA -> BB54NN : All Saint's House, Aspen Lane, Oswaldtwistle, Accrington, Lancashire
            "100012392479",  # BB53RG -> BB53RJ : Usha Lounge Restaurant, Haslingden Old Road, Oswaldtwistle, Accrington
            "100012544307",  # BB50LN -> BB50LR : St. Peter's Vicarage, 151 Willows Lane, Accrington, Lancashire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100010431355",  # BB56LH -> BB56LF : 1 Pipers Row, Huncoat, Accrington, Lancashire
            "100012392809",  # BB56HA -> BB56UE : Woodside House, Burnley Road, Huncoat, Accrington, Lancashire
            "10009970822",  # BB67WA -> BB67UQ : The Bungalow, 27 Mill Lane, Great Harwood, Blackburn, Lancashire
            "100012533996",  # BB14JJ -> BB14LL : 1B Henry Street, Rishton, Blackburn, Lancashire
            "100012392555",  # BB52DL -> BB52DZ : Higher Hey Cottage, Kings Highway, Accrington, Lancashire
            "10009971952",  # BB53SW -> BB53SL : Nigher Friar Hill Farm, Roundhill Road, Accrington, Lancashire
            "100012544405",  # BB50QR -> BB50SH : 43 Fountain Street, Accrington, Lancashire
            "100012392714",  # BB52JX -> BB50NY : Pine Lodge, Rothwell House, Priestley Clough, Accrington, Lancashire
            "100012392419",  # BB51SW -> BB51SP : Church View Home For the Elderly, Emma Street, Accrington, Lancashire
            "10070894405",  # BB50DN -> BB50DP : 74A Market Street, Church, Accrington, Lancashire
            "100012392942",  # BB53JB -> BB53EG : 230A Union Road, Oswaldtwistle, Accrington, Lancashire
            "100012545127",  # BB56DH -> BB51AR : Broadway Hotel, Burnley Road, Accrington, Lancashire
            "10009967793",  # BB50PS -> BB53BB : 5 High Street, Accrington, Lancashire
        ]:
            rec["accept_suggestion"] = False

        return rec
