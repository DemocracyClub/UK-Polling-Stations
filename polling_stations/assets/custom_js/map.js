"use strict";

window.PollingStationMap = function(div_id) {

    var map = L.map(div_id, { zoomControl: true, dragging: !L.Browser.mobile });
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
            prefix: 'fa',
        });

        var station = L.marker(station_point, {
            'clickable': true,
            'icon': stationMarker,
            'title': "Your polling station",
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
                    'icon': homeMarker,
                    'title': "Your home",

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
                    L.featureGroup(markers.concat(directions_polyline)).getBounds(), {
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

window.VotingHubsMap = function(div_id) {

    var map = L.map(div_id, { zoomControl: true, dragging: !L.Browser.mobile });
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

    return {
        draw: function(hub_points, user_location, embed, tile_layer, mq_key) {
            if (embed) {
                map.scrollWheelZoom.disable();
            }

            add_tile_layer(tile_layer, mq_key);

            hub_points.forEach(function(hub) {
                var hubMarker = L.ExtraMarkers.icon({
                    icon: 'fa-check-square',
                    markerColor: 'purple',
                    iconColor: 'white',
                    shape: 'circle',
                    prefix: 'fa',
                });
                var marker = L.marker(hub.point, {
                    clickable: true,
                    icon: hubMarker,
                    title: hub.name,
                });
                var popupHtml = '<strong>' + hub.name + '</strong>';
                if (hub.opening_times && hub.opening_times.length > 0) {
                    popupHtml += '<br><strong>Opening times:</strong>';
                    hub.opening_times.forEach(function(ot) {
                        popupHtml += '<br>' + ot[0] + ': ' + ot[1] + ' \u2014 ' + ot[2];
                    });
                }
                marker.bindPopup(popupHtml);
                marker.addTo(map);
                markers.push(marker);
            });

            if (user_location) {
                var homeMarker = L.ExtraMarkers.icon({
                    icon: 'fa-home',
                    markerColor: 'purple',
                    iconColor: 'white',
                    shape: 'circle',
                    prefix: 'fa',
                });
                var home = L.marker(user_location, {
                    clickable: true,
                    icon: homeMarker,
                    title: 'Your address',
                });
                home.addTo(map);
                markers.push(home);
            }

            if (markers.length > 1) {
                map.fitBounds(
                    L.featureGroup(markers).getBounds(), {
                        maxZoom: 14,
                        padding: [30, 30]
                    }
                );
            } else if (markers.length === 1) {
                map.setView(markers[0].getLatLng(), 15);
            }
        }
    };

};
