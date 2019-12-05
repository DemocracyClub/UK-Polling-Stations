from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000029"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # These polling places have a UPRN, and the addressbase postcode doesn't match
        # the postcode from the council. In these cases the addressbase postcode matches
        # the postcode used on the venue's website.
        # Online references toStation ID 7680 (Whar Hall Road Community Centre) don't
        # align with addressbase, but the postcodes are adjacent. So leaving postcode
        # as is in the CSV.
        if record.polling_place_id == "7518":  # Barston Memorial Institute
            record = record._replace(polling_place_postcode="B92 0JU")
        if record.polling_place_id == "7550":  # St Clements Church
            record = record._replace(polling_place_postcode="B36 0BA")
        if record.polling_place_id == "7561":  # Kingshurst Evangelical Church
            record = record._replace(polling_place_postcode="B37 6NP")
        if (
            record.polling_place_id == "7626"
        ):  # The Royal British Legion (Knowle) Club Limited
            record = record._replace(polling_place_postcode="B93 9LU")
        if record.polling_place_id == "7660":  # Woodlands Campus
            record = record._replace(polling_place_postcode="B36 0NF")

        # Fixes carried forward
        # Three Trees Community Centre
        if record.polling_place_id == "7571":
            record = record._replace(polling_place_uprn="100071461342")
        # Dorridge Methodist Church
        if record.polling_place_id == "7586":
            record = record._replace(polling_place_uprn="100071001475")

        rec = super().station_record_to_dict(record)

        # Tudor Grange Leisure Centre
        if record.polling_place_id == "7726":
            rec["location"] = Point(-1.7881577, 52.4124167, srid=4326)

        # Catherine de Barnes Village Hall
        if record.polling_place_id == "7515":
            rec["location"] = Point(-1.7382134, 52.4203089, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10090949380":
            rec["postcode"] = "B93 0FH"

        if (record.addressline1, record.addressline2) == (
            "101 Noble Way",
            "Cheswick Green",
        ):
            rec["uprn"] = "10090950327"
            rec["accept_suggestion"] = True

        if uprn in [
            "10090945527",  # B377RN -> B376RL : 3C Woodlands Way, Chelmsley Wood
            "10090945525",  # B377RN -> B376RL : 3A Woodlands Way, Chelmsley Wood
        ]:
            rec["accept_suggestion"] = True

        if record.addressline6 in [
            "B90 4AY",  # stray odd-looking property
            "CV7 7HL",  # single property with spurious-looking station
        ]:
            return None

        if uprn in [
            "100071001341",  # B911DA -> B911JW : 90 Grange Road, Solihull
            "10090946742",  # B901FT -> B930EJ : Apartment 16, Leasowes House, 3 Main Street, Dickens Heath, Solihull
            "10090948318",  # B901GL -> B913AB : Apartment 5, Market Court, 61 Old Dickens Heath Road, Shirley, Solihull
            "10090947804",  # CV49BN -> B901FT : 12 Eagle Drive, Solihull
            "200003834455",  # B927AW -> B927AH : St Michaels Residential Home, 251 Warwick Road, Solihull
            "10090946771",  # B920JP -> B930FD : Caravan Firs Farm, Barston Lane, Solihull
            "10090948319",  # B912AW -> B913AB : Flat 2, 58 Lode Lane, Solihull
            "100070965323",  # B376ES -> B376EU : 77 Overgreen Drive, Kingshurst
            "100070965320",  # B376ES -> B376EU : 77A Overgreen Drive, Kingshurst
            "100070965321",  # B376ES -> B376EU : 77B Overgreen Drive, Kingshurst
            "100070965322",  # B376ES -> B376EU : 77C Overgreen Drive, Kingshurst
        ]:
            rec["accept_suggestion"] = False

        return rec
