var markers = []
var the_map;


function general_map_marker (name, where, map) {
    result = new google.maps.Marker ({
	'position' : new google.maps.LatLng( where[0], where [1])
	, 'map' : map
	, 'title': name // TODO add more interesting info.
    });
    return result
}

function addSimpleMap(mapInstance) {
    the_map = mapInstance
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    for (var i = 0; i < map_data.length; i++) {
        if (map_data[i]['where'][0] != 0) {
	        markers.push ( general_map_marker (map_data[i]['name'], map_data[i]['where'], mapInstance ));	        
        }
    }
    show_breakdown_numbers();
}


function show_breakdown_numbers () {
    // suggest ways to break down the search.
    //If you narrow the search by checking more boxes,how many spots would remain on the map ?
    breakdown_object = JSON.parse(jQuery ('#breakdown')[0].innerHTML)
    facets = {
         'habitat' : jQuery ('input[name="trap_habitat"]')
        ,'species' : jQuery ('input[name="trap_species"]')
        ,'school'  : jQuery ('input[name="trap_school" ]')
    }    
    jQuery.each ( facets, show_breakdown_for_facet);
        
}

function show_breakdown_for_facet (the_facet, the_checkboxes) {
    // console.log (the_facet);
    // console.log (the_checkboxes);
    for (var i = 0; i < the_checkboxes.length; i++) {
        the_checkbox = the_checkboxes[i];
        how_many = breakdown_object[the_facet] [the_checkbox.value]
        if ( how_many ) {
            // console.log (the_checkbox);
            // console.log (the_checkbox.value);
            // console.log (how_many);
            jQuery(the_checkbox).next(how_many);
            jQuery(the_checkbox.parentElement).append ( ' (' + how_many + ')' )
        }
    }
}



