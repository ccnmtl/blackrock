function addBlock(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    
    block_json = JSON.parse(jQuery('#block_json')[0].innerHTML);
    trap_sites = JSON.parse(jQuery('#trap_sites')[0].innerHTML);
    
    var box = block_json;
    var rect = make_grid_rectangle (bounds (block_json), mapInstance);
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));
    
    viewer_location = user_location(mapInstance);
    
    radius = parseFloat(jQuery ('#radius_of_circles')[0].value);
    
    for (var i = 0; i < trap_sites.length; i++) {
        trap_info = trap_sites[i];
        circle = x_meter_circle (trap_info['point'], mapInstance, radius);
        attach_marker_info (circle, trap_info);
    }
    
    
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
}

function attach_marker_info(the_circle, info) {    
    function circle_on () {
        jQuery ('#point_' + info['point_id']).addClass("highlighted");
        the_circle.setOptions({fillColor : "blue"});
    }
    function circle_off () {
        jQuery ('#point_' + info['point_id']).removeClass("highlighted");
        the_circle.setOptions({fillColor : "lightgreen"});
    }
    google.maps.event.addListener(the_circle, 'mouseover', circle_on);
    jQuery ('#point_' + info['point_id']).mouseover(circle_on);
    
    google.maps.event.addListener(the_circle, 'mouseout', circle_off);
    jQuery ('#point_' + info['point_id']).mouseout( circle_off );
}

function x_meter_circle (center, map, radius) {
  return  new google.maps.Circle({
      center:  lat_lng_from_point(  center  ),
      radius: radius, //meters 
      map: map,
      fillColor: 'lightgreen',
      strokeWeight : 1,
      strokeColor : 'lightgreen',
      strokeOpacity : 0.3,
   });
}

