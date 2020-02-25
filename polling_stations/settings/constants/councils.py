# settings for councils scraper

YVM_LA_URL = "https://www.yourvotematters.co.uk/_design/nested-content/results-page2/search-voting-locations-by-districtcode?queries_distcode_query="  # noqa
BOUNDARIES_URL = "https://ons-cache.s3.amazonaws.com/Local_Authority_Districts_April_2019_Boundaries_UK_BFE.geojson"


# The data we need won't all be
# updated before May 2019
# so this will help us to bodge it
OLD_TO_NEW_MAP = {
    # Fife
    "S12000015": "S12000047",
    # Perth & Kinross
    "S12000024": "S12000048",
    # Glasgow
    "S12000046": "S12000049",
    # North Lanarkshire
    "S12000044": "S12000050",
    # Somerset West & Taunton
    "E07000190": "E07000246",
    "E07000191": "E07000246",
    # Bournemouth, Christchurch & Poole
    "E06000028": "E06000058",
    "E06000029": "E06000058",
    "E07000048": "E06000058",
    # Dorset
    "E07000049": "E06000059",
    "E07000050": "E06000059",
    "E07000051": "E06000059",
    "E07000052": "E06000059",
    "E07000053": "E06000059",
    # East Suffolk
    "E07000205": "E07000244",
    "E07000206": "E07000244",
    # West Suffolk
    "E07000201": "E07000245",
    "E07000204": "E07000245",
}

NEW_COUNCILS = ["E07000246", "E06000058", "E06000059", "E07000244", "E07000245"]
