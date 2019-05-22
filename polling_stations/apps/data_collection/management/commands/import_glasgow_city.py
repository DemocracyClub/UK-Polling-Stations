from data_collection.management.commands import BaseScotlandSpatialHubImporter

"""
Note:
This importer provides coverage for 245/258 districts
due to incomplete/poor quality data
"""


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000046"
    council_name = "Glasgow City"
    elections = []

    def district_record_to_dict(self, record):
        """
        There's been a boundary change, some datasets have caught up,
        others haven't. Conveniently the 'transfer area' from Glagow to
        North Lanarkshire corresponds neatly to polling district PR2021.
        So for now we're throwing it away.
        """
        if record[0] == "PR2021":
            return None

        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        """
        Throw away the polling station that corresponds to discarded
        polling district as well.
        """
        if record[0] == "PR2021":
            return None

        # The following stations have a diagreement between the stations file and the districts file. So for now we'll throw the stations away.

        if (
            record[0] == "AN3723"
        ):  # Jordanhill Parish Church Hall, Munro Road (28 Woodend Drive), G13 1QT vs   KELVINDALE PRIMARY SCHOOL, 11 DORCHESTER PLACE, G12 0BP 55
            return None
        if (
            record[0] == "CC1007"
        ):  # Our Lady of the Annunciation Primary School, 80 Friarton Road, G43 2PR  vs NEWLANDS SOUTH PARISH CHURCH HALL, 37 RIVERSIDE ROAD, G43 2EG   55
            return None
        if (
            record[0] == "KE2822"
        ):  # St Mungo's Primary School, 45 Parson Street, G4 0RZ vs LADYWELL COMMUNITY HALL, 32A DRYGATE, G4 0YB    44
            return None
        if (
            record[0] == "KE1416"
        ):  # Dunard Street Primary School, 65 Dunard Street, G20 6RL vs MACKINTOSH CHURCH, 870 GARSCUBE ROAD, G20 7EL   44
            return None
        if (
            record[0] == "KE1215"
        ):  # Belhaven Nursery, 54 Kelvinside Avenue, G20 6PY vs KELBOURNE PARK PRIMARY SCHOOL, 109 HOTSPUR STREET, G20 8LH  42
            return None
        if (
            record[0] == "MS1515"
        ):  # Kelvindale Primary School, 11 Dorchester Place, G12 0BP vs ST MARY'S (MARYHILL) PRIMARY SCHOOL, 2 KILMUN STREET, G20 0EL   38
            return None
        if (
            record[0] == "CC0407"
        ):  # City Building Depot, 32 Greenholme Street, G44 4DU vs  CATHCART CONGREGATIONAL CHURCH HALL, 15 GARRY STREET, G44 4AY   38
            return None
        if (
            record[0] == "PR3717"
        ):  # St Philomena's Primary School, 21 Robroyston Road, G33 1EA vs  ALL SAINTS SECONDARY SCHOOL, 299 RYEHILL ROAD, G21 3EN  37
            return None
        if (
            record[0] == "MS4416"
        ):  # St Blane's Primary School, 23 Arrcoher Drive, G23 5QB vs   CADDER PRIMARY SCHOOL, 60 HERMA STREET, G23 5AR 34
            return None
        if (
            record[0] == "MS2016"
        ):  # St Blane's Primary School, 23 Arrocher Drive, G23 5QB vs   CADDER PRIMARY SCHOOL, 60 HERMA STREET, G23 5AR 34
            return None
        if (
            record[0] == "KE2311"
        ):  # Gaelic School, 147 Berkeley Street, G3 7HP vs  HILLHEAD PRIMARY SCHOOL, 110 OTAGO STREET, G12 8NS  29
            return None
        if (
            record[0] == "PK1703"
        ):  # Ashpark Primary School, 75 Kyleakin Road, G46 8DQ vs   DARNLEY PRIMARY SCHOOL, 169 GLEN MORRISTON ROAD, G53 7HT    26
            return None
        if (
            record[0] == "PR3517"
        ):  # All Saints Primary School, 299 Ryehill Road, G21 3EN vs    ALL SAINTS SECONDARY SCHOOL, 299 RYEHILL ROAD, G21 3EN  6
            return None
        return super().station_record_to_dict(record)
