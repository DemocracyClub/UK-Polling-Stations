from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000029"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019soli.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019soli.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # The Loft Above Asda
        if record.polling_place_id == "6826":
            record = record._replace(polling_place_uprn="010023647341")

        # Tudor Grange Leisure Centre
        if record.polling_place_id == "7027":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.7881577, 52.4124167, srid=4326)
            return rec

        # Three Trees Community Centre
        if record.polling_place_id == "6824":
            record = record._replace(polling_place_uprn="100071461342")

        # Elmwood Place
        if record.polling_place_id in ["7041", "7011"]:
            record = record._replace(polling_place_uprn="10090946409")

        # Auckland Hall
        if record.polling_place_id == "7004":
            record = record._replace(polling_place_uprn="200003829755")

        # Dorridge Methodist Church
        if record.polling_place_id == "7081":
            record = record._replace(polling_place_uprn="100071001475")

        # Catherine de Barnes Village Hall
        if record.polling_place_id == "6777":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.7382134, 52.4203089, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090949380":
            rec["postcode"] = "B93 0FH"

        if uprn in [
            "10090945527",  # B377RN -> B376RL : 3C Woodlands Way, Chelmsley Wood
            "10090945525",  # B377RN -> B376RL : 3A Woodlands Way, Chelmsley Wood
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100071001341",  # B911DA -> B911JW : 90 Grange Road, Solihull
            "10090946742",  # B901FT -> B930EJ : Apartment 16, Leasowes House, 3 Main Street, Dickens Heath, Solihull
            "10090948318",  # B901GL -> B913AB : Apartment 5, Market Court, 61 Old Dickens Heath Road, Shirley, Solihull
            "200003823593",  # B904EA -> B946QT : The Flat Cheswick Green Inn, Tanworth Lane, Shirley, Solihull
            "10090947460",  # B904LG -> B377NZ : 18 Archer Drive, Solihull
            "10090947804",  # CV49BN -> B901FT : 12 Eagle Drive, Solihull
            "200003834455",  # B927AW -> B927AH : St Michaels Residential Home, 251 Warwick Road, Solihull
            "10090946771",  # B920JP -> B930FD : Caravan Firs Farm, Barston Lane, Solihull
            "10090946731",  # B377WA -> B930EJ : Apartment 23, Fillingham Court, 66 Fillingham Close, Chelmsley Wood
            "10090946121",  # B913EP -> B920LD : Apartment 10, Scarlet Oak, 911-913 Warwick Road, Solihull
            "10090948319",  # B912AW -> B913AB : Flat 2, 58 Lode Lane, Solihull
            "100070965323",  # B376ES -> B376EU : 77 Overgreen Drive, Kingshurst
            "100070965320",  # B376ES -> B376EU : 77A Overgreen Drive, Kingshurst
            "100070965321",  # B376ES -> B376EU : 77B Overgreen Drive, Kingshurst
            "100070965322",  # B376ES -> B376EU : 77C Overgreen Drive, Kingshurst
            "10023648240",  # B946DQ -> B946DE : 66B Salter Street, Hockley Heath
            "200003831389",  # B360UD -> B360UF : 275 Windward Way, Smith`s Wood
        ]:
            rec["accept_suggestion"] = False

        return rec
