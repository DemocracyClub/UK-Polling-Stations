from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2025-09-25/2025-08-29T13:17:31.958974/Democracy_Club__25September2025.tsv"
    )
    stations_name = (
        "2025-09-25/2025-08-29T13:17:31.958974/Democracy_Club__25September2025.tsv"
    )
    elections = ["2025-09-25"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Set new polling stations easting and northing if at existing polling place
        # St Andrew's Church, Brownley Road, Wythenshawe, Manchester
        if record.polling_place_id == "15066":
            record = record._replace(
                polling_place_easting="382862",
                polling_place_northing="386725",
            )
        # Woodhouse Park Lifestyle Centre, Portway, Woodhouse Park, Manchester
        if record.polling_place_id == "15064":
            record = record._replace(
                polling_place_easting="382019",
                polling_place_northing="386394",
            )
        return super().station_record_to_dict(record)
