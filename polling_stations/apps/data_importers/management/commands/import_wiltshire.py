from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = "2021-07-26/WiltsDemocracy_Club__19August2021.tsv"
    stations_name = "2021-07-26/WiltsDemocracy_Club__19August2021.tsv"
    elections = ["2021-08-19"]
    csv_delimiter = "\t"

    # Checked 63862 (out of council area) and 64258/64219 proximity.

    # These were found because they weren't geocodeable, and so are presumably wrong
    station_postcode_fixes = {
        # Easterton Village Hall, Easterton, Devizes
        # https://wvha.org.uk/listing/easterton-village-hall/
        ("63510", "SN10 4P"): "SN10 4PS",
        # Edington Parish Hall, Edington, Westbury
        ("64399", ""): "",
        # Tidworth Community Centre, Wylye Road Tidworth
        # https://tidworthtowncouncil.gov.uk/tidworth-community-centre/
        ("63590", "SP9 7QH"): "SP9 7QQ",
        # Beanacre Church Schoolroom, Beanacre, Melksham
        ("64478", "SN12"): "",
        # Great Bedwyn Cricket Club, Frog Lane, Great Bedwyn, Marlborough
        # http://www.wccl.org.uk/team_info.php?id=1247
        ("63542", "SN8 3PD"): "SN8 3PB",
        # Wilton Community Centre, West Street, Wilton, Salisbury
        # https://wvha.org.uk/listing/wilton-community-centre/
        ("63870", "SP2 0DJ"): "SP2 0DG",
        # Easton Royal Village Hall, Easton Royal, Pewsey
        # https://wvha.org.uk/listing/easton-royal-village-hall/
        ("63514", ""): "SN9 5LY",
        # Baydon Young Peoples Hall, Baydon, Marlborough
        # http://www.baydon.org/BYPA.htm
        ("63447", ""): "SN8 2JE",
    }

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id,
            record.polling_place_postcode,
        ) in self.station_postcode_fixes:
            record = record._replace(
                polling_place_postcode=self.station_postcode_fixes[
                    (record.polling_place_id, record.polling_place_postcode)
                ]
            )

        return super().station_record_to_dict(record)

    #
    def address_record_to_dict(self, record):
        if record.addressline6.strip() in [
            "SN8 4AF",
            "SN10 4AD",
            "SN10 3SQ",
            "SN8 1QB",
            "SP4 9QE",
            "SN10 3DD",
            "SN10 5HE",
            "SN10 2PA",
            "SN8 3DY",
            "SP5 2BZ",
            "SP5 2NL",
            "SP5 2DT",
            "SP4 8JD",
            "SP4 7PB",
            "SN11 0PQ",
            "SN5 0AB",
            "SN16 9ES",
            "BA13 4LY",
            "SN15 3SX",
            "SN11 8EJ",
            "SN15 5EY",
            "BA14 7DW",
            "SP4 7FF",
            "SN15 3RW",
            "SN5 4HB",
            "SN8 4NR",
            "SN14 6HT",
            "SN10 3EZ",
            "SP3 6DY",
            "SN10 4QP",
            "SN8 1HG",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
