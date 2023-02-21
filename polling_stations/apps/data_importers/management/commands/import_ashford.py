from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASF"
    addresses_name = "2021-03-18T09:55:17.756012/Ashford Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-18T09:55:17.756012/Ashford Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004389187",  # MOBILE HOME AT CLOVER FARM THE PINNOCK, PLUCKLEY
            "200001880702",  # THE CHAPEL, FRITH ROAD, ALDINGTON, ASHFORD
            "200004382948",  # OAKDENE, STATION ROAD, PLUCKLEY, ASHFORD
        ]:
            return None

        if record.addressline6 in ["TN25 7AS", "TN26 3LL"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Rainbow Room, Tenterden Leisure Centre, Recreation Ground Road, Tenterden, Ashford, Kent, TN30 6RA - postocde was in address line 4 so reorganised data
        if record.polling_place_id == "8050":
            record = record._replace(
                polling_place_address_4="Kent", polling_place_postcode="TN30 6RA"
            )

        return super().station_record_to_dict(record)
