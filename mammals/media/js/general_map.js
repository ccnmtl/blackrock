function general_map_marker (name, where, map) {
    result = new google.maps.Marker ({
	'position' : new google.maps.LatLng( where[0], where [1])
	, 'map' : map
	, 'title': name // TODO add more interesting info.
    });
    return result
}

var markers = []
var the_map; // TODO remove
function addSimpleMap(mapInstance) {
    the_map = mapInstance
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    for (var i = 0; i < map_data.length; i++) {
        if (map_data[i]['where'][0] != 0) {
	        markers.push ( general_map_marker (map_data[i]['name'], map_data[i]['where'], mapInstance ));
	        
        }
    }
    add_heatmap_ground_overlay()
}



function add_heatmap_ground_overlay() {
    //TODO get this from settings.py. These bounds are also repeated in generate_ground_overlay_heatmaps .
    blackrock_north = 41.43000 ;
    blackrock_south = 41.37000 ;
    blackrock_east = -73.98000 ;
    blackrock_west = -74.07000 ;
    
    the_bounds = new google.maps.LatLngBounds (
        new google.maps.LatLng( blackrock_south, blackrock_west),
        new google.maps.LatLng( blackrock_north, blackrock_east)
    )
    options = { 'map' : the_map }
    heatmap_image_url = jQuery('#heatmap_image')[0].innerHTML;
    var new_overlay = new google.maps.GroundOverlay(heatmap_image_url, the_bounds, options );
}

