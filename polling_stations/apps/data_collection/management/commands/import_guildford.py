from data_collection.geo_utils import fix_bad_polygons
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 27700
    districts_srid = 27700
    council_id = "E07000209"
    elections = ["parl.2019-12-12"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Guildford"
    geom_type = "gml"

    def replace_schema(self, record):
        """
        Shoddy workaround for:
        Failed to connect to www2.guildford.gov.uk port 80: Connection timed out

        This is *definitely* not the correct way to do this
        but it gets the job done
        """
        record["geometry"] = record["geometry"].replace(
            "http://www2.guildford.gov.uk/ishare5.2.web/getows.ashx?mapsource=GBC/Inspire&amp;service=WFS&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=DescribeFeatureType&amp;TYPENAME=polling_districts&amp;OUTPUTFORMAT=XMLSCHEMA",
            "",
        )
        record["geometry"] = record["geometry"].replace(
            "http://www2.guildford.gov.uk/ishare5.2.web/getows.ashx?mapsource=GBC/Inspire&amp;service=WFS&amp;SERVICE=WFS&amp;VERSION=1.1.0&amp;REQUEST=DescribeFeatureType&amp;TYPENAME=polling_places&amp;OUTPUTFORMAT=XMLSCHEMA",
            "",
        )
        return record

    def district_record_to_dict(self, record):
        record = self.replace_schema(record)
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        return {
            "internal_council_id": record["register"],
            "name": record["pollingdistrictname"],
            "area": poly,
            "polling_station_id": record["register"],
        }

    def station_record_to_dict(self, record):
        record = self.replace_schema(record)
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        return {
            "internal_council_id": record["register"],
            "postcode": "",
            "address": "%s\n%s" % (record["pollingplace"], record["thoroughfare_name"]),
            "location": location,
        }

    def post_import(self):
        fix_bad_polygons()
