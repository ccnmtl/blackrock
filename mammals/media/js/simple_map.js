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
    animals = JSON.parse(jQuery('#animals')[0].innerHTML);
    for (var i = 0; i < animals.length; i++) {
        if (animals[i]['where'][0] != 0) {
	        markers.push ( animal_marker (animals[i]['name'], animals[i]['where'], mapInstance ));
        }
    }
}

function show_squares (difficulty_level) {
    // show all the squares up to and including a particular level of difficulty of access.
    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq ['access_difficulty'] > difficulty_level) {
            axe_square (sq);
        } else {
            sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']  );
            attach_info (sq);
        }
    }
}
