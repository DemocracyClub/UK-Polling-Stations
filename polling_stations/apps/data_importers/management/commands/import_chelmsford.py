from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2026-03-05/2026-02-23T10:07:26.370972/Democracy_Club__07May2026 (3).tsv"
    )
    stations_name = (
        "2026-03-05/2026-02-23T10:07:26.370972/Democracy_Club__07May2026 (3).tsv"
    )
    elections = ["2026-03-05"]
    csv_delimiter = "\t"

    # WARNING: Geocoding with UPRN. Station record postcode does not match addressbase postcode.
    # Station address: 'Rettendon Memorial Hall, Main Road, Rettendon, Chelmsford, CM3 8DR' (id: 14871)
    # File postcode matches gov website, given late date ignoring the warning
    # https://register-of-charities.charitycommission.gov.uk/en/charity-search/-/charity-details/301383/contact-information

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091441445",  # DAIRY FARM COTTAGE, CHELMER VILLAGE WAY, CHELMER VILLAGE, CHELMSFORD, CM2 6TD
                "10093928515",  # CARAVAN 2 AT OAKVALE DOMSEY LANE, LITTLE WALTHAM, CHELMSFORD, CM3 3PS
                "200004627211",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMER VILLAGE, CHELMSFORD, CM2 6NP
                "100091430409",  # BASSMENT NIGHTCLUB, 16-18 WELLS STREET, CHELMSFORD, CM1 1HZ
                "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD, CM2 7TD
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "CM1 7AR",
            "CM1 1FU",
            "CM3 1ER",
            "CM4 0LT",
            "CM4 9JL",
        ]:
            return None

        return super().address_record_to_dict(record)
