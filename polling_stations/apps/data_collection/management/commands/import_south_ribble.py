from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000126"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-13sr.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-13sr.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in ["PR25 2YH", "PR5 4EN"]:
            return None

        if uprn in [
            "100012756794",  # PR53PH -> PR251XB : 85 Leyland Lane, Leyland, Lancashire
            "100012412465",  # PR45JL -> PR45JN : Odd House Farm Hall Carr Lane, Longton, Lancashire
            "10033050400",  # PR10UX -> PR10UY : 22 Broad Oak Lane, Penwortham, Lancashire
            "10033050401",  # PR10UX -> PR10UY : 24 Broad Oak Lane, Penwortham, Lancashire
            "10033050403",  # PR10UX -> PR10UY : 28 Broad Oak Lane, Penwortham, Lancashire
            "10033044689",  # PR55AU -> PR45AU : 146B Liverpool Road, Longton, Lancashire
            "10013243828",  # PR50JD -> PR50JJ : Oak Tree Cottage Bells Lane, Hoghton, Lancashire
            "10033048969",  # PR55RE -> PR55RD : 38A Watkin Lane, Lostock Hall, Lancashire
            "100012757116",  # PR54JA -> PR54JR : 133 Chorley Road, Walton-Le-Dale, Lancashire
            "10033057924",  # PR55UP -> PR55UN : 231 Todd Lane North, Lostock Hall, Lancashire
            "10033057925",  # PR55UP -> PR55UN : 233 Todd Lane North, Lostock Hall, Lancashire
            "10033048429",  # PR55UP -> PR55UN : 235 Todd Lane North, Lostock Hall, Lancashire
            "200002854539",  # PR267PA -> PR267PB : 78 Longmeanygate, Midge Hall, Leyland, Lancashire
            "100010623692",  # PR44LB -> PR44LD : Chain House Farm 115 Chain House Lane, Whitestake, Lancashire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100012412616",  # PR19YT -> PR19YE : The Oaks Hill Road South, Penwortham, Lancashire
            "200001130049",  # PR45JX -> PR45JB : Rydal Mount Liverpool Road, Much Hoole, Lancashire
            "100012412471",  # PR45XB -> PR45ZD : Beech Lodge 9 Hall Lane, Longton, Lancashire
            "10013245106",  # PR50JT -> PR50JS : Campton House Daub Hall Lane, Hoghton, Lancashire
            "10033045703",  # PR55RD -> PR55LA : Pleasant Retreat Watkin Lane, Lostock Hall, Lancashire
            "10013245011",  # PR45SL -> PR45SP : Anchor Inn 86 Liverpool Road, Hutton, Lancashire
            "10033039467",  # PR56BJ -> PR56BA : The Poachers Tavern Cuerden Way, Bamber Bridge, Lancashire
            "100012412971",  # PR19HY -> PR19JA : St Leonards Vicarage Marshalls Brow, Penwortham, Lancashire
            "10013243618",  # PR253UF -> PR253UT : 88 Parish Gardens, Leyland, Lancashire
            "100012413498",  # PR56QE -> PR56RN : The Woodsman School Lane, Bamber Bridge, Lancashire
        ]:
            rec["accept_suggestion"] = False

        return rec
