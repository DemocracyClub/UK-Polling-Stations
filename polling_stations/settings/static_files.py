from dc_utils.settings.pipeline import (  # noqa
    get_pipeline_settings,
    STATICFILES_FINDERS,
)

PIPELINE = get_pipeline_settings(
    extra_css=["scss/style.scss", "font-awesome/css/font-awesome.min.css"],
    extra_js=[],
)

PIPELINE["STYLESHEETS"].update(
    {
        "map": {
            "source_filenames": [
                "leaflet/dist/leaflet.css",
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
        "jquery": {
            "source_filenames": [
                "jquery/dist/jquery.min.js",
            ],
            "output_filename": "js/jquery.js",
        },
        "dashboard": {
            "source_filenames": [
                "leaflet.markercluster/dist/leaflet.markercluster.js",
            ],
            "output_filename": "js/dashboard.js",
        },
        "file_uploads": {
            "source_filenames": [
                "promise-polyfill/dist/polyfill.min.js",
                "jquery/dist/jquery.min.js",
            ],
            "output_filename": "js/file_uploads.js",
        },
    }
)
