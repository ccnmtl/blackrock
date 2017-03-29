
actual_location_circles  = {};

function add_trails_to_mini_map (map) {
    map_options = {
        preserveViewport : true
        , clickable       : true
    };

    buildings_map = new google.maps.KmlLayer(STATIC_URL + "kml/portal/buildings.kml", map_options);
    trail_map = new google.maps.KmlLayer(STATIC_URL + "kml/portal/trails.kml", map_options);
    road_map = new google.maps.KmlLayer(STATIC_URL + "kml/portal/roads.kml", map_options);
    
    trail_map.setMap (map);
    road_map.setMap (map);
    buildings_map.setMap (map);
}

function add_team_form_maps() {
    return; // this is no longer being used. Saving for archival purposes :)
    the_divs  = jQuery ('.team_form_map');
    
    console.log (the_divs);
    maps = {};
    for (var i = 0; i < the_divs.length; i++) {
      the_div = the_divs [i];
      console.log (the_div);
      point_id = parseInt(the_div.id.split("_")[1]);
      
      //center coordinates for map (the coordinates of the suggested location of the point):
        lat = jQuery ('#lat_' + point_id).html();
        lon = jQuery ('#lon_' + point_id).html();
      
       var myOptions = {
          center: new google.maps.LatLng(lat, lon)
          ,zoom: 19
          ,mapTypeId: google.maps.MapTypeId.SATELLITE
          ,mapTypeControl : false
          ,overviewMapControl: false
          ,streetViewControl: false
          ,zoomControl: false
          ,draggable: false
          ,scrollwheel:false
        };
        
        
        maps [i] = new google.maps.Map(the_div, myOptions);
        console.log (maps[i]);
        add_trails_to_mini_map(maps[i]);
        team_form_circle ([lat, lon], mini_map_suggested_point_style, maps[i]);
        transect_center = [
            parseFloat(jQuery ('#transect_center_lat_' + point_id).html())
           ,parseFloat(jQuery ('#transect_center_lon_' + point_id).html())
        ];
        suggested_location = [
            parseFloat(jQuery ('#lat_' + point_id).html())
           ,parseFloat(jQuery ('#lon_' + point_id).html())
        ];
        actual_location = [
            parseFloat(jQuery ('#actual_lat_' + point_id)[0].value)
           ,parseFloat(jQuery ('#actual_lon_' + point_id)[0].value)
        ];
        transect_edge = [
            parseFloat(jQuery ('#transect_edge_lat_'   + point_id).html())
           ,parseFloat(jQuery ('#transect_edge_lon_'   + point_id).html())
        ];
        //team_form_circle (transect_center, mini_map_center_style, maps[i])
        actual_location_circles[point_id] = team_form_circle (actual_location, mini_map_actual_point_style, maps[i]);
        jQuery ('.coord_input').focusout (point_id, actual_location_adjusted);
        // draw the grid square itself.
        corners_of_square = JSON.parse(jQuery('#corner_obj')[0].innerHTML);
        make_grid_rectangle (bounds (corners_of_square),  maps[i]);
        mini_map_transect (lat_lng_from_point(transect_center), lat_lng_from_point(suggested_location), maps[i], mini_map_transect_1_style);
        mini_map_transect (lat_lng_from_point(suggested_location), lat_lng_from_point(transect_edge), maps[i], mini_map_transect_2_style);
    
    }
}
function is_valid_coordinate ( str) {
    return (str.match (/^(\-)?(\d){2}\.(\d){5}$/g) != null);
}


function mini_map_transect (center, edge, map, style) {
    pl=  new google.maps.Polyline(
    {
        path: [center, edge],
        map : map,
    });
    pl.setOptions ( style );
    return pl;
    
}

function hide_trap_info_if_not_used() {
    the_divs  = jQuery ('.team_form_map');
    for (var i = 0; i < the_divs.length; i++) {
        the_div = the_divs [i];
        point_id = parseInt(the_div.id.split("_")[1]);
        switch_id_string = '#whether_a_trap_was_set_here_' + point_id;
        detail_select_ids = [
            '#trap_type_' +  point_id,
            '#bait_' +  point_id,
            '#bait_still_there_' +  point_id,
            '#animal_' +  point_id,
        ];
        
        if (jQuery (switch_id_string + ' option:selected')[0].value == "True") {
            for (var j = 0; j < detail_select_ids.length; j++) {
                jQuery(detail_select_ids[j]).show();
            }
        } else {
            for (var j = 0; j < detail_select_ids.length; j++) {
                jQuery(detail_select_ids[j]).hide();
            }    
        }
    }
}


function update_actual_location_circles() {
    
    the_divs  = jQuery ('.team_form_map');
    for (var i = 0; i < the_divs.length; i++) {
      the_div = the_divs [i];
      point_id = parseInt(the_div.id.split("_")[1]);
    
      if (is_valid_coordinate   (jQuery ('#actual_lat_' + point_id)[0].value)
        &&  is_valid_coordinate (jQuery ('#actual_lon_' + point_id)[0].value) ) {
            if (not_too_far_away (point_id)) {  
              redraw_actual_location_point (point_id);
            }
            else {
                console.log ('TOO FAR AWAY');
                reset_actual_location (point_id);
            
            }
       }
       else {
            reset_actual_location (point_id);
       }
    }
}


function not_too_far_away (point_id) {
    /// don't allow the actual trap to get too far away from the suggested location.
    // http://stackoverflow.com/questions/1502590/calculate-distance-between-two-points-in-google-maps-v3
    //fifty_meters =  0.05 // kilometers
    //twenty_meters =  0.02 // kilometers
    //five_meters =  0.005 // kilometers
    
    two_hundred_fifty_meters =  0.25; // kilometers
    
    
    suggested_location = lat_lng_from_point([
        parseFloat(jQuery ('#lat_'   + point_id).html()).toFixed(5)
       ,parseFloat(jQuery ('#lon_'   + point_id).html()).toFixed(5)
    ]);
    actual_location = lat_lng_from_point([
        parseFloat(jQuery ('#actual_lat_' + point_id)[0].value)
        ,parseFloat(jQuery ('#actual_lon_' + point_id)[0].value)
    ]);
    return (distHaversine ( suggested_location, actual_location) < two_hundred_fifty_meters);
    
}

function redraw_actual_location_point (point_id) {
    actual_location = [
        parseFloat(jQuery ('#actual_lat_' + point_id)[0].value)
        ,parseFloat(jQuery ('#actual_lon_' + point_id)[0].value)
    ];
    actual_location_circles[point_id].setCenter(lat_lng_from_point(actual_location));

}

function reset_actual_location (point_id) {
   suggested_location = [
        parseFloat(jQuery ('#lat_'   + point_id).html()).toFixed(5)
       ,parseFloat(jQuery ('#lon_'   + point_id).html()).toFixed(5)
   ];
    jQuery ('#actual_lat_' + point_id)[0].value = suggested_location[0];
    jQuery ('#actual_lon_' + point_id)[0].value = suggested_location[1];

}

function actual_location_adjusted (arg1, arg2) {
    update_actual_location_circles();
}

function team_form_circle (center, style, map) {
  c = new google.maps.Circle({
      center:  lat_lng_from_point(  center  ),
      map: map,
   });
  c.setOptions (style);
  return  c;
}

function team_form_init() {
    hide_trap_info_if_not_used();
    jQuery ('.whether_a_trap_was_set_here_dropdown').change(hide_trap_info_if_not_used);
}

function save_team_form_ajax (){
    jQuery.ajax({
        data: jQuery('#team_form').serialize(),
        type: 'POST',
        url: '/mammals/save_team_form_ajax/',
        success: function(response) {
            alert ('Team information saved.' );
        }
    });
    return false;
}

jQuery(team_form_init);
