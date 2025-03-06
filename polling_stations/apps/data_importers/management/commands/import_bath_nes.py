from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAS"
    addresses_name = "2025-05-01/2025-03-06T16:39:35.399261/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-06T16:39:35.399261/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]

    # Postcode conflicts for below stations are approved by the council, ignore warnings.
    # (26) The Pavilion, East Harptree Playing Fields, East Harptree, BS40 6BH
    # (29) Farmborough Memorial Hall, Little Lane, Farmborough, BA2 0AE
    # (54) Council Chamber, The Hollies, High Street, Midsomer Norton, BA3 2DP
    # (85) Bishop Sutton Village Hall, Wick Road, Bishop Sutton, BS39 5XD
    # (43) St Mary's Parish Centre, Burlington Street, Bath, BA1 2SA
    # (57) Weston Methodist Church Hall, Kennington Road, Bath, BA1 3PR
    # (50) Beechen Cliff Methodist Church Hall, Bruton Avenue, Bath, BA2 4RF
    # (94) Hayesfield Girls' School, Brougham Hayes Gym, Entrance via Staff Car Park, Brougham Hayes, BA2 3QX
    # (71) Priston Village Hall, High Street, Priston, BA2 9EE
    # (81) Saltford Hall, Wedmore Road, Saltford, BS31 3BY
    # (91) Ubley Village Hall, The Street, Ubley, BS40 6PN
    # (94) Hayesfield Girls' School, Brougham Hayes Gym, Entrance via Staff Car Park, Brougham Hayes, BA2 3QX

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094952037",  # KINGSHILL FARM, BRISTOL ROAD, COMPTON MARTIN, BRISTOL
            "100120029109",  # 15 UPPER BLOOMFIELD ROAD, BATH
            "10093714965",  # THE STABLE, GIBBET LANE, BRISTOL
        ]:
            return None

        if record.housepostcode in [
            # split
            "BA2 6DR",
            "BA2 5AD",
            "BA2 2RZ",
            # suspect
            "BA3 5SF",
        ]:
            return None
        return super().address_record_to_dict(record)
