from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WBK"
    addresses_name = (
        "2024-05-02/2024-03-19T11:25:52.770139/Democracy_Club__02May2024v2.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-19T11:25:52.770139/Democracy_Club__02May2024v2.CSV"
    )
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Peasemore Village Hall Peasemore RG20 7JE
        if record.polling_place_id == "8390":
            record = record._replace(
                polling_place_postcode="RG20 7JE ",
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
