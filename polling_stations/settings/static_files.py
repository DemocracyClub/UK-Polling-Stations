from dc_theme.settings import get_pipeline_settings
from dc_theme.settings import STATICFILES_FINDERS
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = STATICFILES_FINDERS + (
    'pipeline.finders.ManifestFinder',
)

PIPELINE = get_pipeline_settings(
    extra_css=[
        'custom_css/style.scss',
        'font-awesome/css/font-awesome.min.css',
    ],
    extra_js=[],
)
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE['UGLIFYJS_BINARY'] = 'node_modules/uglify-js/bin/uglifyjs'
PIPELINE['UGLIFYJS_ARGUMENTS'] = '--no-mangle'
PIPELINE['STYLESHEETS']['map'] = {
    'source_filenames': [
        'leaflet/dist/leaflet.css',
        'custom_css/map.css',
        'leaflet-extra-markers/dist/css/leaflet.extra-markers.min.css',
    ],
    'output_filename': 'css/map.css',
}
PIPELINE['JAVASCRIPT']['map'] = {
    'source_filenames': [
        'leaflet/dist/leaflet.js',
        'leaflet-extra-markers/dist/js/leaflet.extra-markers.min.js',
        '@mapbox/polyline/src/polyline.js',
        'custom_js/polyline_global.js',
    ],
    'output_filename': 'js/map.js',
}
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
