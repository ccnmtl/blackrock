function addBlock(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    var block_json = JSON.parse(jQuery('#block_json')[0].innerHTML);
    var transects   =JSON.parse(jQuery('#transects_json')[0].innerHTML);
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
    // if the square is really small, do something

    
    var dot_radius;
    var side_of_square =  distHaversine (lat_lng_from_point(box[0]) , lat_lng_from_point(box[1] )) * 1000; //meters.
    var really_small_square =(side_of_square < 150 );
    if ( really_small_square ) {
        dot_radius = side_of_square / 50;
        initial_circle_style.radius = dot_radius;
        circle_off_style.radius = dot_radius;
        circle_on_style.radius = dot_radius * 2;
    
    }
    else {
        dot_radius = 2.0;
    }
    
    var center = lat_lng_from_point(box[4]);
    for (var i = 0; i < transects.length; i++) {
        var transect_obj = transects[i];
        var new_transect = transect (center, lat_lng_from_point(transect_obj.edge), mapInstance);
        for (var j = 0; j < transects[i]['points'].length; j++) {
            var next_point = transects[i]['points'][j];
            var circle = x_meter_circle (next_point['point'], mapInstance);
            attach_marker_info (circle, next_point, new_transect, transect_obj);
        }
    }
    
    jQuery ('#hide_square_coords_table_button').click (hide_square_coords_table);
    jQuery ('#show_square_coords_table_button').click (show_square_coords_table);
    hide_square_coords_table();
    
}

function hide_square_coords_table () {
    jQuery ('.square_coords_table_div').hide();
    jQuery ('#hide_square_coords_table_button').hide();
    jQuery ('#show_square_coords_table_button').show();
}

function show_square_coords_table () {
    jQuery ('.square_coords_table_div').show();
    jQuery ('#hide_square_coords_table_button').show();
    jQuery ('#show_square_coords_table_button').hide();
}

function hide_all_except_printer_friendly_table() {
    jQuery('#printer_friendly_table').show();
    jQuery('#right_hand_table').hide();
    jQuery ('#show_printer_friendly_table').hide();
    jQuery ('#hide_printer_friendly_table').show();
}


function hide_printer_friendly_table() {
    jQuery('#printer_friendly_table').hide();
    jQuery('#right_hand_table').show();
    jQuery ('#show_printer_friendly_table').show();
    jQuery ('#hide_printer_friendly_table').hide();
}



/// Some decoration functions for drawing the map:

function attach_marker_info (the_circle, point_info, the_transect, transect_info) {

    jQuery ('#show_printer_friendly_table').click(hide_all_except_printer_friendly_table);
    jQuery ('#hide_printer_friendly_table').click(hide_printer_friendly_table);
    hide_printer_friendly_table();

    // When the mouse is over a circle or its corresponding row in the table,
    // highlight both the circle and its table row.
    var table = jQuery ('#transect_table_overflow_div');
    var transect_row = table.find( '.transect_'    + point_info['transect_id']);
    //transect_top = transect_row.position().top
    var transect_top = 100;
    var point_id_row = jQuery ('.top_px_number.point_' + point_info['point_id']);
    
    
    var row_top = jQuery ('.get_row_top_from_here.point_' + point_info['point_id']).position().top;
    
    // this is the hidden column that contains the "top" value we want to scroll to:
    point_id_row.html(row_top);
    
    
    function circle_on (scroll_into_view) {
        // Add some nice css classes to the table:
        jQuery ('.point_'    + point_info['point_id']).addClass("highlighted"); 
        jQuery ('.transect_' + point_info['transect_id']).addClass("highlighted");
        point_id_row = jQuery ('.top_px_number.point_' + point_info['point_id']);
        if (scroll_into_view) {
            var offset = 194;
            var goal = Number(point_id_row.html()) - jQuery ('#transect_table_overflow_div').position().top - offset;
            jQuery ('#transect_table_overflow_div').animate({scrollTop: goal}, { duration: 500, queue: false });
        }    
        // change the decoration of the circle and transect
        
        the_circle.setOptions(circle_on_style);
        the_transect.setOptions (transect_on_style);
    }
    // Unhighlight a circle:
    function circle_off () {
        jQuery ('.point_'    + point_info['point_id']).removeClass("highlighted");
        jQuery ('.transect_' + point_info['transect_id']).removeClass("highlighted");
        the_circle.setOptions(circle_off_style);
        the_transect.setOptions (transect_off_style);
    }
    
    function circle_on_from_map () {
        scroll_into_view = true;
        circle_on (scroll_into_view);
    }
    
    function circle_on_from_table () {
        scroll_into_view = false;
        circle_on (scroll_into_view);
    }
    
    
    google.maps.event.addListener(the_circle, 'mouseover', circle_on_from_map);
    google.maps.event.addListener(the_circle, 'mouseout', circle_off);
    jQuery ('.point_'    + point_info['point_id']).mouseover (circle_on_from_table);
    jQuery ('.point_'    + point_info['point_id']).mouseout (circle_off);
}

function x_meter_circle (center, map) {
    var c = new google.maps.Circle({
        center:  lat_lng_from_point(  center  ),
        map: map,
   });
    c.setOptions (initial_circle_style);

  return  c;
}

function transect (center, edge, map) {
    var pl =  new google.maps.Polyline(
    {
        path: [center, edge],
        map : map,
    });
    pl.setOptions ( initial_transect_style );
    return pl;
    
}

function confirm_new_bearings(){
    var ok = true;
    var error_msg = "Sorry, you can't have more than 20 bearings, or more than 10 traps on each transect.";
    if (parseInt(jQuery('#num_transects')[0].value) > 20) {
        jQuery('#num_transects')[0].value = "20";
        ok = false;
    }
    
    if (parseInt(jQuery('#points_per_transect')[0].value) > 10) {
        jQuery('#points_per_transect')[0].value = "10";
        ok = false;
    }

    if (!ok) {
        alert (error_msg);
        return false;
    }

    return confirm("Are you sure you want to generate new bearings? \n This will erase the ones currently displayed.");
}


function new_expedition_ajax (){
    jQuery.ajax({
        data: jQuery('#new_start_expedition_form').serialize(),
        type: 'POST',
        url: '/mammals/new_expedition_ajax/',
        success: function(response) {
            jQuery(jQuery('#save_square_via_ajax')[0]).hide();
            //jQuery('#save_square_via_ajax').hide();
            alert ('This information has been saved as Expedition #' + response + '.');
        }
    });
    return false;
}
