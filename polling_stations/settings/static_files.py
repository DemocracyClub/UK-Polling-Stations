from dc_utils.settings.pipeline import (  # noqa
    get_pipeline_settings,
    STATICFILES_FINDERS,
    STATICFILES_STORAGE,
)

PIPELINE = get_pipeline_settings(
    extra_css=["scss/style.scss", "font-awesome/css/font-awesome.min.css"],
    extra_js=[],
)
AWS_S3_OBJECT_PARAMETERS = {"Cache-Control": "max-age=315576000, immutable"}

PIPELINE["STYLESHEETS"].update(
    {
        "map": {
            "source_filenames": [
                "leaflet/dist/leaflet.css",
                "custom_css/map.css",
                "leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css",
            ],
            "output_filename": "css/map.css",
        },
        "dashboard": {
            "source_filenames": [
                "leaflet.markercluster/dist/MarkerCluster.css",
                "leaflet.markercluster/dist/MarkerCluster.Default.css",
            ],
            "output_filename": "css/dashboard.css",
        },
    }
)

PIPELINE["JAVASCRIPT"].update(
    {
        "map": {
            "source_filenames": [
                "jquery/dist/jquery.min.js",
                "leaflet/dist/leaflet.js",
                "leaflet-extra-markers/dist/js/leaflet.extra-markers.min.js",
                "@mapbox/polyline/src/polyline.js",
                "custom_js/polyline_global.js",
                "custom_js/map.js",
            ],
            "output_filename": "js/map.js",
        },
        "dashboard": {
            "source_filenames": [
                "leaflet.markercluster/dist/leaflet.markercluster.js",
            ],
            "output_filename": "js/dashboard.js",
        },
    }
)
