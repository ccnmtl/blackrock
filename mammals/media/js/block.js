function addBlock(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    block_json = JSON.parse(jQuery('#block_json')[0].innerHTML);
    transects   =JSON.parse(jQuery('#transects_json')[0].innerHTML);
    var box = block_json;
    var rect = make_grid_rectangle (bounds (block_json), mapInstance);
    
    // make sure the square actually shows on the map:
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
    
    center = lat_lng_from_point(box[4]);
    //center_marker_ = draw_center_marker (center, mapInstance);
    point_radius = 2.0
    for (var i = 0; i < transects.length; i++) {
        transect_obj = transects[i];
        new_transect = transect (center, lat_lng_from_point(transect_obj['edge']), mapInstance)
        for (var j = 0; j < transects[i]['points'].length; j++) {
            next_point = transects[i]['points'][j];
            circle = x_meter_circle (next_point['point'], mapInstance, point_radius);
            attach_marker_info (circle, next_point, new_transect, transect_obj);
        }
    }
    
}


/// Some decoration functions for drawing the map:

function attach_marker_info (the_circle, point_info, the_transect, transect_info) {
    // When the mouse is over a circle or its corresponding row in the table,
    // highlight both the circle and its table row.
    
    function circle_on () {
        // Add some nice css classes to the table:
        jQuery ('.point_'    + point_info['point_id']).addClass("highlighted"); 
        jQuery ('.transect_' + point_info['transect_id']).addClass("highlighted");
        // change the decoration of the circle and transect
        the_circle.setOptions({fillColor : "blue", radius:5, zIndex: 1});
        the_transect.setOptions ({strokeOpacity : 1, });
    }
    // Unhighlight a circle:
    function circle_off () {
        jQuery ('.point_'    + point_info['point_id']).removeClass("highlighted");
        jQuery ('.transect_' + point_info['transect_id']).removeClass("highlighted");
        the_circle.setOptions({fillColor : "lightgreen", radius:2, zIndex: 2});
        the_transect.setOptions ({strokeOpacity : 0.3, });
    }
    google.maps.event.addListener(the_circle, 'mouseover', circle_on);
    google.maps.event.addListener(the_circle, 'mouseout', circle_off);
    jQuery ('.point_'    + point_info['point_id']).mouseover (circle_on);
    jQuery ('.point_'    + point_info['point_id']).mouseout (circle_off);
}

function x_meter_circle (center, map, radius) {
  return  new google.maps.Circle({
      center:  lat_lng_from_point(  center  ),
      radius: radius, //meters 
      map: map,
      fillColor: 'lightgreen',
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'lightgreen',
      strokeOpacity : 1,
      zIndex: 1
   });
}

function transect (center, edge, map) {
    return polyline = new google.maps.Polyline(
    {
        path: [center, edge], 
        strokeColor : 'red',
        strokeOpacity : 0.3, 
        zIndex: -3,
        map : map,
    });
}

function draw_center_marker (center, map) {
  return  new google.maps.Circle({
      center: center,
      radius: 2.0,
      fillColor: 'red',
      strokeWeight : 1,
      fillOpacity : 1,
      strokeColor : 'red',
      strokeOpacity : 1,
      map: map
   });
}

