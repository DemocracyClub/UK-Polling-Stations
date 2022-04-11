from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2022-05-05/2022-03-25T10:48:40.698958/Democracy_Club__05May2022.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-25T10:48:40.698958/Democracy_Club__05May2022.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # 'Queen Elizabeth Hall Annexe, New Cut, Layer-de-la-Haye, Colchester, CO2 0EH' (id: 11290)
        if record.polling_place_id == "11290":
            record = record._replace(polling_place_postcode="CO2 0EG")

        # 'Old Heath Community Centre, D`Arcy Road, Old Heath, Colchester, CO2 8BB' (id: 11385)
        if record.polling_place_id == "11385":
            record = record._replace(polling_place_postcode="CO2 8BA")

        # 'Rowhedge Village Hall, Rectory Road, Rowhedge, Colchester, CO5 7HX' (id: 11387)
        if record.polling_place_id == "11387":
            record = record._replace(polling_place_postcode="CO5 7HR")

        # 'Paxman Academy, Paxman Avenue, Colchester, Essex, CO2 9DQ' (id: 11454)
        if record.polling_place_id == "11454":
            record = record._replace(polling_place_postcode="CO2 9DB")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093741451",  # 82 MALDON ROAD, TIPTREE, COLCHESTER
            "10093741447",  # 84A MALDON ROAD, TIPTREE, COLCHESTER
            "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER
        ]:
            return None

        if record.addressline6 in [
            "CO4 3GQ",  # across another area; very close to another station
            # split
            "CO4 5LG",
            "CO2 8BU",
            "CO6 1HA",
        ]:
            return None

        return super().address_record_to_dict(record)
