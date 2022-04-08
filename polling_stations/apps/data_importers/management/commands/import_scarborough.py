from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SCE"
    addresses_name = (
        "2022-05-05/2022-04-08T14:06:10.359669/polling_station_export-2022-04-07.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-08T14:06:10.359669/polling_station_export-2022-04-07.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Hackness Village Hall, Red Hill, Hackness, Scarborough, YO13 OBT
        if record.pollingstationnumber == "13":
            record = record._replace(
                pollingstationpostcode="YO13 0JW"
            )  # UPRN 10012897671

        # Muston Village Hall, Carr Lane, Muston, Filey, YO14 OEN
        if record.pollingstationnumber == "27":
            record = record._replace(
                pollingstationpostcode="YO14 0EN"
            )  # UPRN 200003339210

        # Sports Pavilion, Grosmont
        if record.pollingstationnumber == "57":
            # Believe this is at 482557.02,505294.89, but it's not in AddressBase. Given postcode is far away.
            # On OSM: https://www.openstreetmap.org/way/66640406
            record = record._replace(pollingstationpostcode="")  # was YO22 5QJ

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "YO21 1SU",
            "YO12 5DB",
            "YO14 9EW",
            "YO11 3NH",
            "YO21 3JU",
            "YO21 3FP",
            "YO21 1XD",
            "YO11 3PQ",
        ]:
            return None

        if record.uprn.lstrip("0") in [
            "10023875937",  # 3 POSTGATE WAY, UGTHORPE, WHITBY
            "10091090917",  # 30 HIGHFIELD ROAD, WHITBY
        ]:
            return None

        return super().address_record_to_dict(record)
