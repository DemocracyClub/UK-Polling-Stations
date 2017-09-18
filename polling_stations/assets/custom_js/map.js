"use strict";

window.PollingStationMap = function(div_id) {

    var map = L.map(div_id, {zoomControl:true, dragging: !L.Browser.mobile});
    var markers = [];

    var add_tile_layer = function(tile_layer, mq_key) {
        var tiles;
        if ((tile_layer == 'MapQuestSDK') && (mq_key)) {
          $.getScript("http://www.mapquestapi.com/sdk/leaflet/v2.s/mq-map.js?key=" + mq_key).done(function() {
            tiles = MQ.tileLayer();
            tiles.addTo(map);
          });
        }
        if (tile_layer == 'OpenStreetMap') {
          tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
            subdomains: 'abc'
          });
          tiles.addTo(map);
        }
      };

      var add_station_marker = function(station_point) {
        var stationMarker = L.ExtraMarkers.icon({
          icon: 'fa-check-square',
          markerColor: 'purple',
          iconColor: 'white',
          shape: 'circle',
          prefix: 'fa'
        });

        var station = L.marker(station_point, {
          'clickable': true,
          'icon': stationMarker
        });
        station.addTo(map);
        markers.push(station);
      };

      var add_directions = function(directions) {
        var homeMarker = L.ExtraMarkers.icon({
          icon: 'fa-home',
          markerColor: 'purple',
          iconColor: 'white',
          shape: 'circle',
          prefix: 'fa'
        });

        if (directions.route) {
          var decoded = polyline.decode(directions.route, directions.precision);
          try {
            var firstpolyline = new L.Polyline(decoded, {
              color: 'red',
              weight: 3,
              opacity: 1.0,
              smoothFactor: 1,
              dashArray: "5, 5"
            });

            // home
            var home = L.marker(firstpolyline._latlngs[0], {
              'clickable': true,
              'icon': homeMarker
            });
            home.addTo(map);
            markers.push(home);

            firstpolyline.addTo(map);
            return firstpolyline;
          } catch (e) {
            // do nothing
            // if something goes wrong trying to plot the route
            // we only want to show the station point
          }
        }
        return false;
      };

      return {
        draw: function(station_point, embed, tile_layer, mq_key, directions) {
          if (embed) {
            map.scrollWheelZoom.disable();
          }

          add_tile_layer(tile_layer, mq_key);
          add_station_marker(station_point);
          var directions_polyline = add_directions(directions);

          if ((markers.length == 2) && directions_polyline) {
            map.fitBounds(
                L.featureGroup(markers.concat(directions_polyline)).getBounds(),
                {
                  maxZoom: 16,
                  padding: [30, 30]
                }
            );
          } else {
            map.setView(station_point, 15);
          }
        }

      };

};
