# settings for councils scraper

YVM_LA_URL = "https://www.yourvotematters.co.uk/_design/nested-content/results-page2/search-voting-locations-by-districtcode?queries_distcode_query="  # noqa
BOUNDARIES_URL = (
    "https://opendata.arcgis.com/datasets/593018bf59ab4699b66355bd33cd186d_1.geojson"
)


# The data we need won't all be
# updated before May 2019
# so this will help us to bodge it
OLD_TO_NEW_MAP = {
    # Fife
    "S12000015": "S12000047",
    # Perth & Kinross
    "S12000024": "S12000048",
}
