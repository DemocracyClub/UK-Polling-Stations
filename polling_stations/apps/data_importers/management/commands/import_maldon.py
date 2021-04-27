from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAL"
    addresses_name = "2021-04-19T13:28:23.590902/Maldon Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-19T13:28:23.590902/Maldon Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094633716",  # PARK HOUSE MALDON ROAD, LATCHINGDON
            "200000918556",  # PLOT E5 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10014001292",  # PLOT D2 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10013998717",  # CARAVAN C6 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "200000916950",  # PLOT E48 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10014000997",  # PLOT C19 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10013998650",  # PLOT D45 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "200000916798",  # PLOT E36 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10014001505",  # PLOT C23 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "10014001698",  # PLOT B11 BARROW MARSH CARAVAN SITE GOLDHANGER ROAD, HEYBRIDGE
            "100091258201",  # FLAT MILL BEACH PUBLIC HOUSE GOLDHANGER ROAD, HEYBRIDGE
            "200000910329",  # ROSEWOOD LODGE, HOWE GREEN ROAD, PURLEIGH, CHELMSFORD
        ]:
            return None

        if record.addressline6 in ["CM8 3LS", "CM9 4NY", "CM9 6HR"]:
            return None

        return super().address_record_to_dict(record)
