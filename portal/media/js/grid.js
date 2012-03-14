function addGrid(mapInstance) {

    
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    for (var i = 0; i < grid_json.length; i++) {
        for (var j = 0; j < grid_json[i].length; j++) {
            box = grid_json[i][j]
            
            // draw the box:
            make_grid_rectangle (bounds (box), mapInstance);
            
            // add a marker at the center of the box:
            marker = new google.maps.Marker({ 
                position: location(box[4]),
                map: mapInstance
            });
            
        }
    }
    mapInstance.setMapType(G_SATELLITE_MAP);

    
}

function bounds (box) {
    var bl  = location(box[0]);
    var tl  = location(box[1]);
    var tr  = location(box[2]);
    var br  = location(box[3]);
    return [ bl, tl, tr, br];
}

function make_grid_rectangle (_paths, mapInstance) {
    rect = new google.maps.Polygon ({
        paths           : _paths,
        fillOpacity     : 0.1,
        fillColor       : 'blue',
        strokeOpacity   : 0.3,
        strokeColor     : 'green',
        strokeWeight    : 1,
        map             : mapInstance
    });
}

function location(point ) {
    return new google.maps.LatLng(point[0] , point[1]);
}
