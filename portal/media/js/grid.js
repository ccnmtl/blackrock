function addGrid(mapInstance) {

    
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    
    for (var i = 0; i < grid_json.length; i++) {
        for (var j = 0; j < grid_json[i].length; j++) {
            box = grid_json[i][j]
            rect = make_grid_rectangle (bounds (box), mapInstance);
            /*
            marker = new google.maps.Marker({ 
                position: location(box[4]),
                map: mapInstance
            });
            */
            attach_info (rect, { 'i':  i,  'j':  j, 'box':box } )           
        }
    }
    
    
    // why you no work?
    //mapInstance.setMapType(G_SATELLITE_MAP);
   
}


//closure:
function attach_info(rect, info) {
  google.maps.event.addListener(rect, 'mouseup', function() {
  
  
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0])
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1])
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2])
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3])
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4])
  
    //alert (info);
  });
}

function trimpoint (point) {
    return [point[0].toPrecision(5),point[1].toPrecision(5)]
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
    return rect;
    
    
}

function location(point ) {
    return new google.maps.LatLng(point[0] , point[1]);
}

function amarker (point, map) {
    marker = new google.maps.Marker({ 
        position: location(point),
        map: map
    });
}

function markers (points, map) {
    for (var i = 0; i < points.length; i++) {
       console.log (points[i]);
       amarker (points [i], map);
    }
}

/*
function write (text, point, map) {
    marker = new google.maps.Marker({ 
        position: location(point),
        map: map
    });
}

*/
