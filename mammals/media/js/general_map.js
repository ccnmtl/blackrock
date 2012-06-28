function animal_marker (name, where, map) {
    ppp = new google.maps.LatLng( where[0], where [1]);
    //console.log (ppp);

    result = new google.maps.Marker ({
	'position' : ppp
	, 'map' : map
	, 'title': name
    });
    return result
}

var markers = []

function addSimpleMap(mapInstance) {
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    for (var i = 0; i < map_data.length; i++) {
        if (map_data[i]['where'][0] != 0) {
	        markers.push ( animal_marker (map_data[i]['name'], map_data[i]['where'], mapInstance ));
        }
    }
}
