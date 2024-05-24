from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRC"
    addresses_name = (
        "2024-07-04/2024-05-27T09:27:09.452526/Bracknell_Forest_combined.csv"
    )
    stations_name = (
        "2024-07-04/2024-05-27T09:27:09.452526/Bracknell_Forest_combined.csv"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10022826533",  # THE BUNGALOW OAKWOOD PARK KENNELS PEACOCK LANE, WOKINGHAM
            "200000332122",  # THRUMS, FOLIEJON PARK, WINKFIELD, WINDSOR
        ]:
            return None
        if record.housepostcode in [
            # split
            "SL5 8RY",
            "RG42 6BX",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Binfield Memorial Hall, Terrace Road South, Binfield, BRACKNELL
        # postcode correction from council: RG42 4DJ -> RG42 4DS
        if record.pollingvenueid == "3":
            record = record._replace(pollingstationpostcode="RG42 4DS")

        # 'Bracknell Central Library, Town Square, Bracknell, RG12 1AT' (id: 4495)
        if record.pollingvenueid == "4495":
            record = record._replace(pollingstationpostcode="")

        # 'Bracknell Methodist Church Hall, Shepherds Lane, BRACKNELL, RG42 2DD' (id: 5)
        if record.pollingvenueid == "5":
            record = record._replace(pollingstationpostcode="")

        # 'Bracknell Methodist Church Hall, Shepherds Lane, BRACKNELL, RG42 2DD' (id: 5)
        if record.pollingvenueid == "5":
            record = record._replace(pollingstationpostcode="")

        # 'Bracknell Central Library, Town Square, Bracknell, RG12 1AT' (id: 4495)
        if record.pollingvenueid == "4495":
            record = record._replace(pollingstationpostcode="")

        # 'Sandhurst School Sports Centre, Owlsmoor Road, Owlsmoor, Sandhurst, GU47 0SP' (id: 4018)
        if record.pollingvenueid == "4018":
            record = record._replace(pollingstationpostcode="")

        # 'Sandhurst School Sports Centre, Owlsmoor Road, Owlsmoor, Sandhurst, GU47 0SP' (id: 4018)
        if record.pollingvenueid == "4018":
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
