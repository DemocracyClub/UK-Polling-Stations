"use strict";

$(document).ready(function() {
    document.querySelectorAll('[data-hub-map]').forEach(function(mapDiv) {
        var details = mapDiv.closest('details');
        var initialized = false;

        function initMap() {
            if (!initialized && details.open) {
                initialized = true;
                var hubPoint = [parseFloat(mapDiv.dataset.lat), parseFloat(mapDiv.dataset.lng)];
                var hubDirections = {};
                if (mapDiv.dataset.route) {
                    hubDirections = {
                        route: JSON.parse(mapDiv.dataset.route),
                        precision: parseInt(mapDiv.dataset.precision, 10)
                    };
                }
                var hubMap = new PollingStationMap(mapDiv.id);
                hubMap.draw(hubPoint, embed, tile_layer, mq_key, hubDirections);
            }
        }

        details.addEventListener('toggle', initMap);
        // Initialize immediately if the details is already open
        initMap();
    });
});
