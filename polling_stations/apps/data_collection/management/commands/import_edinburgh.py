from data_collection.github_importer import BaseGitHubImporter

"""
There's no polling station for district EE16L which covers the hospital at Little France
"""


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "S12000036"
    elections = ["europarl.2019-05-23"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Edinburgh"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))

        return {
            "internal_council_id": record["Code2016"],
            "name": record["NEWWARD"] + " - " + record["Code2016"],
            "area": poly,
            "polling_station_id": record["Code2016"],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        codes = record["LG_PP"].split("/")
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            if (
                code == "EC11H"
            ):  # Polling station address changed to match code in Council email
                stations.append(
                    {
                        "internal_council_id": code,
                        "address": "City Chambers,\nHigh Street,\nEdinburgh,\nEH1 1YJ",
                        "postcode": "",
                        "location": None,
                    }
                )
            elif (
                code == "NC05D"
            ):  # Polling station address changed to match code in Council email
                stations.append(
                    {
                        "internal_council_id": code,
                        "address": "FetLor Youth Club,\n122 Crewe Road South,\nEdinburgh,\nEH4 2NY",
                        "postcode": "",
                        "location": None,
                    }
                )

            elif (
                code == "EN12K"
            ):  # Polling station address changed to match code in Council email
                stations.append(
                    {
                        "internal_council_id": code,
                        "address": "Norton Park Conference Centre,\n53 Albion Road,\nEdinburgh,\nEH7 5QY",
                        "postcode": "",
                        "location": None,
                    }
                )
            elif code == "EE16L":  # Code not present in Council email
                pass
            else:
                stations.append(
                    {
                        "internal_council_id": code,
                        "address": "\n".join(
                            [record["Polling__1"], record["Address_1"]]
                        ),
                        "postcode": "",
                        "location": location,
                    }
                )
        return stations
