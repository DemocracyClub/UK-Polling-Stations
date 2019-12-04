from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000032"
    addresses_name = (
        "parl.2019-12-12/Version 2/Bradford Polling Stations_12th December.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Bradford Polling Stations_12th December.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "22845":
            # Toller Youth Café, 2 Duckworth Lane
            record = record._replace(
                polling_place_easting="414102", polling_place_northing="434471"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if (
            record.addressline1.endswith(" All Saints Hall")
            and record.addressline2 == "All Saints Road"
        ):
            record = record._replace(addressline6="BD5 0NZ")

        if record.addressline1 == "4 West Wood View":
            record = record._replace(
                property_urn="10093449448", addressline6="BD10 0FJ"
            )

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010577818",  # BD133SW -> BD133SP : 34 Bottomley Holes, Thornton, Bradford
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100051146371",  # BD62JZ -> BD62JY : Rock House, 200 Cemetery Road, Low Moor, Bradford
            "10010577818",  # BD133SW -> BD133SP : 34 Bottomley Holes, Thornton, Bradford
            "200004700106",  # BD128EW -> BD128EY : 1 Saxon Court, Wyke, Bradford
            "100051272010",  # BD206PE -> BD206FQ : Longlands, Skipton Road, Steeton, Keighley
            "10024070042",  # BD48TJ -> BD48SY : Flat At, 2 Parry Lane, Bradford
            "100051122402",  # BD215RA -> BD215QU : Heather Lodge, Keighley Road, Hainworth Shaw, Keighley
            "200004702084",  # BD133SP -> BD133SW : 36 Cragg Lane, Thornton, Bradford
            "100051150769",  # BD133SP -> BD133SW : The Croft, Cragg Lane, Thornton, Bradford
            "100051935773",  # BD164ED -> BD164TE : Wingfield Nursing Home, Priestthorpe Road, Bingley
            "10010582254",  # BD157WB -> BD157YS : Willowbank Care Village, Bell Dean Road, Allerton, Bradford
        ]:
            rec["accept_suggestion"] = False

        if uprn == "10090402080":
            return None

        if record.addressline6 in [
            "BD4 0BA",
            "BD22 9SX",
            "BD13 3SD",
            "BD13 1NQ",
            "BD13 1NG",
            "BD14 6PY",
            "BD3 8HE",
            "BD21 1RP",
            "BD21 5AB",
            "BD21 2HP",
            "BD17 5DH",
        ]:
            return None

        return rec
