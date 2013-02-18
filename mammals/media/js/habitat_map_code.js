function location_marker (name, where, map) {
    result = new google.maps.Marker ({
	    'position' : new google.maps.LatLng( where[0], where [1])
	    , 'map'    : map
	    , 'title'  : name
    });
    
    return result
}

var markers = []

function addSimpleMap(mapInstance) {
    locations = JSON.parse(jQuery('#animals')[0].innerHTML);
    for (var i = 0; i < locations.length; i++) {
        if (locations[i]['where'][0] != 0) {
	        markers.push ( location_marker (locations[i]['name'], locations[i]['where'], mapInstance ));
        }
    }
}

