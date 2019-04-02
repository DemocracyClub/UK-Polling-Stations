from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000050"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019.CSV"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019.CSV"
    elections = ["local.2019-05-02"]

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3203":
            record = record._replace(polling_place_postcode="CW6 9NA")

        if record.polling_place_id == "3089":
            record = record._replace(polling_place_postcode="CH3 8BJ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100012371869":
            rec["postcode"] = "CW4 7LP"
        if uprn in ["10013203208", "10013201585"]:
            rec["postcode"] = "CW10 0QQ"
        if uprn == "100012371896":
            rec["postcode"] = "WA16 9SG"
        if uprn == "10014519222":
            rec["postcode"] = "WA4 4QG"
        if uprn == "100012371909":
            rec["postcode"] = "WA16 9NQ"

        if record.addressline6.strip() in ["CW7 4AF", "CW8 2QS", "CW8 2JS"]:
            return None

        if uprn in [
            "10013575202",  # CH661NZ -> CH661NT : Station House, Station Road, Little Sutton, Ellesmere Port, Cheshire
            "100012372045",  # WA169JQ -> WA169JH : 1 Laburnum Cottages, Middlewich Road, Allostock, Knutsford, Cheshire
            "100012372046",  # WA169JQ -> WA169JH : 2 Laburnum Cottages, Middlewich Road, Allostock, Knutsford, Cheshire
            "200003238279",  # CW82NQ -> CW72NQ : 3 Salterswall Cottages, Chester Road, Winsford, Cheshire
            "200003237975",  # CW60JQ -> CW69AU : Boot House Farm, Hall Lane, Rushton, Tarporley, Cheshire
            "100012807237",  # WA60AH -> WA60HS : 2 Meadow Farm Cottages, Lower Rake Lane, Helsby, Frodsham, Cheshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10091641303",  # WA169ND -> CH12NW : 2 The Barns, Booth Bed Lane, Allostock, Knutsford, Cheshire
            "200000832753",  # CH36EA -> CH36EE : The Bungalow,Oakfield Nurseries, Saighton Lane, Huntington, Chester, Cheshire
            "200000829308",  # CW60RP -> CH38BH : Weldon Farm, Dog Lane, Kelsall, Tarporley, Cheshire
            "100012353094",  # CW60HA -> CW60ET : The Woodlands, Duddon Heath, Duddon, Tarporley, Cheshire
            "100012603215",  # CW72QN -> CW72QW : 3 Chester Lane Brook, Chester Lane, Marton, Northwich, Cheshire
            "200000830166",  # CH38JU -> CW60NQ : Mill Cottage, Mill Lane, Tarvin, Chester, Cheshire
            "200003331973",  # CH647TD -> CH643TH : Flat, 1 Weatherstones House, Chester High Road, Neston, Cheshire
            "100012571126",  # CH39HN -> CH39HL : Bolesworth Lake Farm, Bolesworth Hill Road, Tattenhall, Chester, Cheshire
        ]:
            rec["accept_suggestion"] = False

        return rec
