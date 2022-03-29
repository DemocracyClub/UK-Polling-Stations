from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOL"
    addresses_name = (
        "2022-05-05/2022-03-22T11:29:47.538214/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-22T11:29:47.538214/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # 'Barston Memorial Institute, Barston Lane, Barston, Solihull, B92 0JN' (id: 9443)
        if record.polling_place_id == "9443":
            record = record._replace(polling_place_postcode="B92 0JU")

        # 'St Clements Church, Green Lane, Corner Clevedon Avenue, Castle Bromwich, Birmingham, B36 0BX' (id: 9359)
        if record.polling_place_id == "9359":
            record = record._replace(polling_place_postcode="B36 0BA")

        # 'KEC Church Centre, Cooks Lane, Kingshurst, Birmingham, B37 6NU' (id: 9268)
        if record.polling_place_id == "9268":
            record = record._replace(polling_place_postcode="B37 6NP")

        # 'Whar Hall Community Centre, Whar Hall Road, Solihull, B92 0PG' (id: 9562)
        if record.polling_place_id == "9562":
            record = record._replace(polling_place_postcode="B92 0PE")

        # 'The Royal British Legion (Knowle) Club Limited, 1611 Warwick Road, Knowle, Solihull, B93 9LF' (id: 9341)
        if record.polling_place_id == "9341":
            record = record._replace(polling_place_postcode="B93 9LU")

        # 'St Peter`s Hall, Holly Lane, Balsall Common, Coventry, CV7 7EA' (id: 9262)
        if record.polling_place_id == "9262":
            record = record._replace(polling_place_postcode="CV7 7FT")

        # 'Woodlands Campus, Solihull College, Auckland Drive, Smith`s Wood, Solihull, B36 0NE' (id: 9323)
        if record.polling_place_id == "9323":
            record = record._replace(polling_place_postcode="B36 0NF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.property_urn.lstrip("0") in [
            "10008213142",  # too far
        ]:
            return None

        if record.addressline6 in [
            "B90 8BW",  # 3 properties embedded in another area
        ]:
            return None

        if record.addressline6 in [
            "B93 9JN",
            "B93 8PP",
            "B37 7RN",
            "B91 1UQ",
            "B92 8NA",
            "B90 3QQ",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
