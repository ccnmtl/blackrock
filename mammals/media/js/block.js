function addBlock(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    
    block_json = JSON.parse(jQuery('#block_json')[0].innerHTML);
    //trap_sites = JSON.parse(jQuery('#trap_sites')[0].innerHTML);
    //test_points =JSON.parse(jQuery('#test_points')[0].innerHTML);
    transects   =JSON.parse(jQuery('#transects_json')[0].innerHTML);
    
    var box = block_json;
    var rect = make_grid_rectangle (bounds (block_json), mapInstance);
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));
    
    center = lat_lng_from_point(box[4]);
    //center_marker_ = draw_center_marker (center, mapInstance);
    
    point_radius = 2.0

    for (var i = 0; i < transects.length; i++) {
        next_transect = transects[i];
        //console.log (transects[i]);
        transect (center, lat_lng_from_point(next_transect['edge']), mapInstance)
        for (var j = 0; j < transects[i]['points'].length; j++) {
            next_point = transects[i]['points'][j];
            circle = x_meter_circle (next_point['point'], mapInstance, point_radius);
            //console.log (next_point);
        }
        //transect (center, lat_lng_from_point(point_info), mapInstance);
        
        //draw_center_marker (lat_lng_from_point(point_info), mapInstance);
        
        /*
        circle = x_meter_circle (trap_info['point'], mapInstance, radius);
        attach_marker_info (circle, trap_info);
        */
    }
    

    /*
    for (var a = 0; a < 360; a+=20) {
        new_point = [];
        new_point = center;
        transect (center, lat_lng_from_point(new_point), mapInstance); 
        console.log (a);
        radians = degrees_to_radians(a);
        with (Math) {
             y = r*sin(theta)
             x = r*cos(theta)
        
        }
        
        console.log ('a');
    }
    */
    
    /*
    viewer_location = user_location(mapInstance);
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    */
    //radius = parseFloat(jQuery ('#radius_of_circles')[0].value);
    radius = 2.0;


    /*
    for (var i = 0; i < trap_sites.length; i++) {
        trap_info = trap_sites[i];
        circle = x_meter_circle (trap_info['point'], mapInstance, radius);
        attach_marker_info (circle, trap_info);
        transect (center, lat_lng_from_point(trap_info['point']), mapInstance);
    }
    */
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
    
}

function degrees_to_radians(angle) {
    return angle * 3.14159263 / 180.0 
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
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'lightgreen',
      strokeOpacity : 1,
   });
}

function transect (center, point, map) {
    var polyline = new google.maps.Polyline(
    {
        path: [ center, point], 
        map : map,
        strokeColor : 'red',
        strokeOpacity : 0.3, 
        zIndex: -3
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
/*
  return  new google.maps.Circle({
      radius: 30.0, //meters 
*/
}

