from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WBK"
    addresses_name = (
        "2024-07-04/2024-06-05T14:00:09.100507/Democracy_Club__04July2024A.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T14:00:09.100507/Democracy_Club__04July2024A.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # extract postcode from address for: Peasemore Village Hall Peasemore, RG20 7JE
        if record.polling_place_id == "9312":
            record = record._replace(
                polling_place_postcode="RG20 7JE",
                polling_place_address_2="",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081027716",  # WOODRIDGE, PRIORS COURT ROAD, HERMITAGE, THATCHAM
            "10093421384",  # NARROWBOAT FOXY LADY MONKEY BRIDGE MOORINGS RUSSELL ROAD, NEWBURY
            "10023919673",  # NARROWBOAT EDWIN DRAGON NORTHCROFT MOORINGS RUSSELL ROAD, NEWBURY
            "10023919674",  # NARROWBOAT GOLDEN ORIOLE NORTHCROFT MOORINGS RUSSELL ROAD, NEWBURY
            "100081027875",  # COLEY FARM, COLEY, STONEY LANE, ASHMORE GREEN, THATCHAM
            "100080242019",  # 2 JAMES LANE, BURGHFIELD, READING
            "100080242018",  # 1 JAMES LANE, BURGHFIELD, READING
            "200001867765",  # 75 FIFTH ROAD, NEWBURY
            "100081026787",  # BRAMLEY HOUSE, BURNT HILL, YATTENDON, THATCHAM
            "10009201450",  # RUSSETT HOUSE, BURNT HILL, YATTENDON, THATCHAM
        ]:
            return None

        if record.addressline6 in [
            # split
            "RG14 5NT",
            "RG7 3RN",
            "RG14 1EP",
        ]:
            return None

        return super().address_record_to_dict(record)
