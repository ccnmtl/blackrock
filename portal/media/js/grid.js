
function addGrid(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    for (var i = 0; i < grid_json.length; i++) {

        var row =  i + 1;

        for (var j = 0; j < grid_json[i].length; j++) {
            var box = grid_json[i][j];
            var rect = make_grid_rectangle (bounds (box), mapInstance);
            
            var column = grid_json[i].length - j;

            attach_info (rect, {
                    'i':  i,
                    'j':  j,
                    'row':  row,
                    'column':  column,
                    'id' : i * grid_json.length  + column,
                    'box':box
                }
                    
            )
            map_bounds.extend(lat_lng_from_point(box[4] ));
        }
    }
    
    
    viewer_location = user_location(mapInstance);
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    
    // why you no work?
    //mapInstance.setMapType(G_SATELLITE_MAP);
    
    
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
}


//closure:
function attach_info(rect, info) {
  google.maps.event.addListener(rect, 'mouseover', function() {
  
    rect.setOptions ({fillOpacity : 0.3});
  
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
    
    
    jQuery('#selected_block_center_y') [0].value = info['box'][4][0];
    jQuery('#selected_block_center_x') [0].value = info['box'][4][1];
    
  
    jQuery('#block_info') [0].innerHTML =  'Block # ' + info['id']+ ':'
    
  });
  
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions ({fillOpacity : 0.1});
  });
  
  
  google.maps.event.addListener(rect, 'click', function() {
    //rect.setOptions ({fillOpacity : 0.1});
    
    
    
   
    
     jQuery('#grid_form')[0].action =   '/portal/grid_block/';
     jQuery('#grid_form')[0].submit();
 
  });
  
  

}

function trimpoint (point) {
    return [point[0].toFixed(3),point[1].toFixed(3)];
}

function bounds (box) {
    var bl  = lat_lng_from_point(box[0]);
    var tl  = lat_lng_from_point(box[1]);
    var tr  = lat_lng_from_point(box[2]);
    var br  = lat_lng_from_point(box[3]);
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


function user_location (mapInstance) {
    var position = false;
    if (typeof(google.loader) != 'undefined' && typeof(google.loader.ClientLocation) != 'undefined') {
        var lat = google.loader.ClientLocation.latitude;
        var lng = google.loader.ClientLocation.longitude;
        if (!isNaN (lat) && !isNaN (lng)) {
            you_are_here (new google.maps.LatLng(lat, lng), mapInstance);
        }
    }
    if (typeof(navigator.geolocation) != 'undefined') {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            you_are_here (new google.maps.LatLng(lat, lng), mapInstance);
        });
    }
    return position;
}
