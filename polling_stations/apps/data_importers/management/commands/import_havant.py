from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAA"
    addresses_name = (
        "2024-05-02/2024-03-13T18:24:56.064221/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T18:24:56.064221/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060449180",  # 161A WEST LANE, HAYLING ISLAND
            "100060449181",  # 161 WEST LANE, HAYLING ISLAND
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PO9 4JG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # point correction for: Queens Inclosure Primary School, Cornelius Drive, Waterlooville, PO7 8NT
        if record.polling_place_id == "7790":
            record = record._replace(polling_place_easting="469447")
            record = record._replace(polling_place_northing="110277")

        # postcode correction for: St Wilfrid`s Lower Church Hall, Padnell Road, Waterlooville, PO8 8DJ
        if record.polling_place_id == "7850":
            record = record._replace(polling_place_postcode="PO8 8DZ")

        # Leigh Park Community Centre, Dunsbury Way , Leigh Park, Havant
        if record.polling_place_id == "7799":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # The following are coordinates from the council:

        # Emsworth Baptist Church, North Street, Emsworth
        if record.polling_place_id == "7778":
            record = record._replace(polling_place_uprn="10013673105")
            record = record._replace(polling_place_easting="474948")
            record = record._replace(polling_place_northing="105930")
        # St Wilfrid`s Lower Church Hall, Padnell Road, Waterlooville
        if record.polling_place_id == "7850":
            record = record._replace(
                polling_place_uprn="100062456104",
                polling_place_easting="469411",
                polling_place_northing="111187",
            )
        # Hart Plain Church, 59 Hart Plain Avenue, Waterlooville
        if record.polling_place_id == "7844":
            record = record._replace(
                polling_place_uprn="100062456214",
                polling_place_easting="468072",
                polling_place_northing="111007",
            )
        # Westbrook Hall, Tempest Avenue, Waterlooville
        if record.polling_place_id == "7856":
            record = record._replace(
                polling_place_uprn="100062672492",
                polling_place_easting="469908",
                polling_place_northing="110223",
            )
        # Cowplain Activity Centre, Padnell Road, Waterlooville
        if record.polling_place_id == "7852":
            record = record._replace(
                polling_place_uprn="10023639981",
                polling_place_easting="469611",
                polling_place_northing="110978",
            )
        # Sports Pavilion, Hollybank Recreation Ground, Southleigh Road, Emsworth
        if record.polling_place_id == "7766":
            record = record._replace(
                polling_place_uprn="10013680948",
                polling_place_easting="474661",
                polling_place_northing="107296",
            )
        # Bedhampton Methodist Church Hall, Park Lane, Havant
        if record.polling_place_id == "7741":
            record = record._replace(
                polling_place_uprn="100062457478",
                polling_place_easting="470303",
                polling_place_northing="106962",
            )
        # St. Nicholas Church Centre, Belmont Grove, Bedhampton, Havant
        if record.polling_place_id == "7737":
            record = record._replace(
                polling_place_uprn="100062457487",
                polling_place_easting="470220",
                polling_place_northing="106739",
            )
        # Barncroft Primary School, Park Lane, Havant
        if record.polling_place_id == "7743":
            record = record._replace(
                polling_place_uprn="100062457467",
                polling_place_easting="470525",
                polling_place_northing="107516",
            )
        # Emsworth Sports & Social Club, 43-45 Havant Road, Emsworth
        if record.polling_place_id == "7782":
            record = record._replace(
                polling_place_uprn="100062400883",
                polling_place_easting="474368",
                polling_place_northing="105973",
            )
        # Cowplain Social Club, 54 London Road, Cowplain, Waterlooville, Hampshire
        if record.polling_place_id == "7840":
            record = record._replace(
                polling_place_uprn="10013672796",
                polling_place_easting="469290",
                polling_place_northing="111260",
            )
        # Bedhampton Community Centre, 21 Bedhampton Road, Bedhampton, Havant
        if record.polling_place_id == "7738":
            record = record._replace(
                polling_place_uprn="10023639958",
                polling_place_easting="470632",
                polling_place_northing="106563",
            )
        # 1st Emsworth Scout Hut, Conigar Road, Emsworth
        if record.polling_place_id == "7770":
            record = record._replace(
                polling_place_uprn="10013667577",
                polling_place_easting="474945",
                polling_place_northing="107336",
            )

        return super().station_record_to_dict(record)
