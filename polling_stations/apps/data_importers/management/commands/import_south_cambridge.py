from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2021-03-16T10:56:43.784190/South Cambridgeshire Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-16T10:56:43.784190/South Cambridgeshire Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008082519",  # DWELLING AT REAR 43 CAMBRIDGE ROAD, WIMPOLE
            "10033031432",  # BURY LANE HOUSE, BURY LANE, MELBOURN, ROYSTON
            "10008079271",  # GREENGAGE COTTAGE, BURY LANE, MELBOURN, ROYSTON
            "10094259590",  # CROWDEAN, CROWDEAN LANE, ELSWORTH, CAMBRIDGE
            "100091203868",  # ANNEXE CLARE BARN MAIN STREET, CALDECOTE
            "200001812525",  # THE GATE HOUSE, ST. NEOTS ROAD, DRY DRAYTON, CAMBRIDGE
            "100091203790",  # FOSTERS LONG DROVE, COTTENHAM
            "100090163907",  # 34 WOODFIELD ROAD, HIGHFIELDS CALDECOTE, CAMBRIDGE
            "100090161038",  # 10 THE PASTURES, HARSTON, CAMBRIDGE
        ]:
            return None

        if record.addressline6 in ["CB23 6LE", "CB24 4QG"]:
            return None

        return super().address_record_to_dict(record)
