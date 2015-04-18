Sometimes it's easier to convert data to formats we know and love.

That reqiures passing incantations to ogr2ogr.

Some of them that have worked previously are listed here.

### Mapinfo -> Shapefile

    $ ogr2ogr -f 'ESRI Shapefile' polling_districts.shp  Polling\ districts\ 2012.TAB
