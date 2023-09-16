from django_assets import Bundle, register


core_css = Bundle(
    'scss/main.scss',
    filters=('scss'),
    depends=('**/*.scss'),
    output='gen/css/main.css'
)

core_js = Bundle(
    'js/jquery.min.js',
    'js/popper.min.js',
    'js/bootstrap/util.js',
    'js/bootstrap/collapse.js',
    'js/bootstrap/dropdown.js',
    filters=('uglifyjs'),
    output="gen/js/main.js"
)


geokey_css = Bundle(
    'geoposition/css/geoposition.css',
    output='gen/css/geokey.css'
)


geokey_js = Bundle(
    'js/geokey.js',
    filters=('uglifyjs'),
    output='gen/js/geokey.js'
)

mobile_js = Bundle(
    'js/mobile.js',
    filters=('uglifyjs'),
    output='gen/js/mobile.js'
)

search_list_map_js = Bundle(
    'js/search-list-map.js',
    filters=('uglifyjs'),
    output='gen/js/searches.js'
)

register('core_css', core_css)
register('core_js', core_js)
register('geokey_css', geokey_css)
register('geokey_js', geokey_js)
register('search_list_map_js', search_list_map_js)
register('mobile_js', mobile_js)
