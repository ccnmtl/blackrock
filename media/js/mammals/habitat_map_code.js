var markers = [];
var the_map;

var recalculate_every_time = false; // recalculate the numbers in parenthesis every time an ajax request is made
// rather than just on page load.

function lat_lng_from_point(point ) {
    return new google.maps.LatLng(point[0] , point[1]);
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
        map             : mapInstance
    });
    rect.setOptions (square_styles['regular']['unselected']);
    rect.setOptions ({visible:false});
    return rect;
}
//addGrid(self.mapInstance)

function to_base_256 (a) {
    var sixteen = 256 / 16;
    return  parseInt(a, 16) * sixteen;
}

function to_google_color (b) {
    var r; var g; var b;
    try {
        r = to_base_256 (b[0]);
    } catch (TypeError) {
        r = 0;
    }
    try {
        g = to_base_256 (b[1]);
    } catch (TypeError) {
        g = 0;
    }
    try {
        b = to_base_256 (b[2]);
    } catch (TypeError) {
        b = 0;
    }
    result =  "rgb(" + r + "," + g + "," + b + ")";
    return result;
}

function decorate_page() {
    // anything that only has to be done once on page load, put here.
    show_little_habitat_disks();
}

function wipe_markers() {
    // No, really.
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
        //delete (markers[i]);
    }
    //delete (markers);
    //markers = [];
    markers.length = 0;
}


function draw_the_grid(the_map) {
    var grid_obj = [];
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML);
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), the_map);
        //grid_json [i]['grid_rectangle'] = rect;
        grid_obj.push (rect);
        add_show_square_mouseover (rect, grid_json[i]['battleship_coords']);
        add_show_square_mouseout  (rect, grid_json[i]['battleship_coords']);
    }
    the_map['grid_obj'] = grid_obj;
}

function show_the_grid(the_map) {
    for (var i = 0; i < the_map.grid_obj.length; i++) {
        the_map.grid_obj[i].setVisible(true);
        
    }
}


function hide_the_grid(the_map) {
    for (var i = 0; i < the_map.grid_obj.length; i++) {
        the_map.grid_obj[i].setVisible(false);
    }
}


function show_or_hide_the_grid (the_map) {
    // show or hide the grid:
    if (jQuery('#id_gridOn').attr('checked')) {
        show_the_grid(the_map);
    }
    else {
        hide_the_grid(the_map);
    }   
}

function contains_checked_boxes (facet_box) {    
    var how_many_are_checked = jQuery (facet_box).next().find('input:checkbox:checked').length;
    return (how_many_are_checked > 0);

}

function basic_turnbuckle_toggle () {
    // accordion toggle:
    if (contains_checked_boxes(this)) {
        // you can't close a facet box if it contains checked boxes.
        return false;
    }
    jQuery(this).next().toggle();
    jQuery(this).toggleClass("ui-corner-all ui-corner-top");
    var child = jQuery(this).children("span.ui-icon");
    child.toggleClass("ui-icon-triangle-1-s ui-icon-triangle-1-e");
    return false;
}


function deal_with_facet_checkbox() {
    //console.log (this);

}

function add_date_boxes() {
    jQuery( "#id_from_date" ).datepicker();
    jQuery( "#id_until_date" ).datepicker();

}

function addHabitatMap(mapInstance) {
    // This function is run ONLY ONCE, on page load.
    // this is called from on high.
    the_map = mapInstance;
    breakdown_object = JSON.parse(jQuery ('#breakdown')[0].innerHTML);
    
    //initial_breakdown_object = JSON.parse(jQuery ('#breakdown')[0].innerHTML);
    
    //alert ('hi');
    //var goat = breakdown_object;
    
    //console.log (goat);
    
    
    
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    refresh_map(mapInstance, breakdown_object, map_data);
    jQuery('.trap_location_checkbox_container input').change(checkbox_change_callback);
    decorate_page();
    draw_the_grid(the_map);
    jQuery('#id_gridOn').change(function  () { show_or_hide_the_grid (the_map);});

    jQuery(".ui-accordion-header").click(basic_turnbuckle_toggle);

    add_date_boxes();
    
    //eddie adding this:
    if (! recalculate_every_time ) {
        show_breakdown_numbers( breakdown_object);
    }
}


function checkbox_change_callback() {
    // set turnbuclkes to gray if they are not empty:
    
    //jQuery(".ui-accordion-header").each(deal_with_facet_checkbox )
    
    var my_accordion = jQuery (this).parents( '.ui-accordion')[0]  ;

    var my_header    = jQuery(my_accordion).children(".ui-accordion-header");
    
    
    var my_triangle = jQuery(my_header).children("span.ui-icon");

    //console.log ( jQuery(my_accordion)    )
    //console.log ( jQuery(my_header)    )

    if (contains_checked_boxes(my_header)) {
       // console.log ("contains checked boxes");
        my_triangle.removeClass("ui-icon-triangle-1-s ui-icon-triangle-1-e ui-icon-triangle-1-l");
        my_triangle.addClass("ui-icon-triangle-1-l");
        
    }
    
    else {
        //console.log ("contains NO checked boxes");
        my_triangle.removeClass("ui-icon-triangle-1-s ui-icon-triangle-1-e ui-icon-triangle-1-l");
        my_triangle.addClass("ui-icon-triangle-1-s");
    
    }
    

    /// and do an ajax search:
    jQuery.ajax({
        data: jQuery('#the_habitat_search_form').serialize(),
        type: 'POST',
        url: '/mammals/ajax_search/',
        success: function(response) {
            //console.log (response);
            var resp_obj = JSON.parse(response);
            //console.log (JSON.stringify (resp_obj['breakdown_object']));
            refresh_map (the_map, resp_obj['breakdown_object'], resp_obj['map_data']);
        }
    });
    return false;
}

function refresh_map (mapInstance, breakdown_object, map_data) {
    wipe_markers();
    var habitat_colors_obj = JSON.parse(jQuery ('#habitat_colors_div')[0].innerHTML);
    function habitat_marker (habitat_id, name, where, map) {
        the_rgb = habitat_colors_obj[habitat_id];
        style = habitat_disk_style;
        style['fillColor'] = to_google_color (the_rgb);
        style['name']      = name;
        c = new google.maps.Circle({
            center:  new google.maps.LatLng( where[0], where [1]),
            map: map,
        });
        c.setOptions (style);
        function show_info_window (event) {
            if (the_map.currently_open_infowindow != undefined) {
                the_map.currently_open_infowindow.close();
            }
            the_infowindow = new google.maps.InfoWindow();
            the_infowindow.setContent( name );
            the_infowindow.setPosition(event.latLng);
            the_infowindow.open(the_map);
            the_map.currently_open_infowindow = the_infowindow;
        }
        google.maps.event.addListener(c, 'click', show_info_window);
        return c;
    }
    for (var i = 0; i < map_data.length; i++) {
        if (map_data[i]['where'][0] != 0) {
            habitat_id = map_data[i]['habitat_id'];        
	        new_marker = habitat_marker (habitat_id,   map_data[i]['name'], map_data[i]['where'], mapInstance );
	        markers.push ( new_marker);
        }
    }
    
    if (recalculate_every_time ){
        show_breakdown_numbers( breakdown_object);
    }
}


function isEmpty(obj) {
    // Stay classy, JavaScript.
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop)) {
            return false;
        }
    }
    return true;
}

function show_breakdown_numbers (breakdown_object) {
    //console.log (JSON.stringify(breakdown_object));
    
    
    jQuery ('.breakdown_number_span').remove();
    
    if (isEmpty (breakdown_object)) {
        console.log ('breakdown object is empty');
        return;
    }
    var facets = {
         'habitat' :       jQuery ('input[name="habitat" ]')
        ,'species' :       jQuery ('input[name="species" ]')
        ,'school'  :       jQuery ('input[name="school"  ]')
        ,'success'  :      jQuery ('input[name="success" ]')
        ,'signs'  :        jQuery ('input[name="signs"   ]')
    };
    
    
    res = [];
    
    
    jQuery.each (facets, function (k, v) { res.push ( {'k': k, 'v': v } ); }  );
    
    for (var j = 0; j < res.length; j++) {
        the_facet      = res[j]['k'];
        the_checkboxes = res[j]['v'];
        for (var i = 0; i < the_checkboxes.length; i++) {

            var the_checkbox = the_checkboxes[i];
            //console.log (the_checkbox);
            //console.log (JSON.stringify (breakdown_object[the_facet]));
            var how_many = breakdown_object[the_facet] [the_checkbox.value];
            //console.log (how_many);
            if ( how_many ) {
                say_how_many (the_checkbox, how_many);
            }
        }
    }
    //console.log (breakdown_object);
    
}


function say_how_many (the_checkbox, how_many) {
    jQuery(the_checkbox.parentElement).append ( '<span class = "breakdown_number_span"> (' + how_many + ') </span>' );
    
}


///// SHOWING SQUARE COORDS:
function add_show_square_mouseover (rect, battleship_coords) {
    google.maps.event.clearListeners(rect, 'mouseover');
    google.maps.event.addListener(rect, 'mouseover', function() {
        rect.setOptions (square_styles['regular']['selected']);
        jQuery ('#battleship_coords_span').html(battleship_coords);
  });
}

function add_show_square_mouseout (rect, thing) {
    google.maps.event.clearListeners(rect, 'mouseout');
    google.maps.event.addListener(rect, 'mouseout', function() {
        rect.setOptions (square_styles['regular']['unselected']);
        jQuery ('#battleship_coords_span').html('');
    });
}


///////////// HABITAT LEGEND DISKS:



function draw_disk_html (disk_path) {
    var withoutLeadingSlash = disk_path[0] === '/' ?
        disk_path.substring(1) :
        disk_path;
    return "<img class='habitat_legend_disk' src='" +
        STATIC_URL + withoutLeadingSlash + "'/>" ;
}

function show_little_habitat_disks() {
    var little_habitat_disks_obj = JSON.parse(jQuery ('#little_habitat_disks_div')[0].innerHTML);
    function show_a_disk (i, checkbox) {
        var habitat_id = checkbox.value;
        var disk_path = little_habitat_disks_obj[habitat_id];
        if (disk_path != '') {
            jQuery(checkbox.parentElement).prepend ( draw_disk_html(disk_path) );    
        }
    }
    jQuery.each (jQuery ('input[name="habitat" ]'), show_a_disk);
}



function close_unused_facets () {


}


function open_or_close_facet(facet_jquery, open) {
    // if open is true, make sure the facet is open
    
    
    // if open is false, make sure the facet is closed.

}

/*
// getter
var active = $( ".selector" ).accordion( "option", "active" );
 
// setter
$( ".selector" ).accordion( "option", "active", 2 );
*/

function facet_is_open  (facet_jquery) {
    // returns boolean true if the facet is open, false if it is closed. 
    
    //var active = $( ".selector" ).accordion( "option", "active" );
    //console.log (active);
    
}


function addTrails (mapObj) {
    var self = mapObj;
    var buildings_kmllayer = new Portal.Layer("roads", STATIC_URL + "kml/portal/buildings.kml", true);
    self.layers["buildings"] = buildings_kmllayer;
    buildings_kmllayer.instance.setMap(self.mapInstance);
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajaxSetup() {
    // setup some ajax progress indicator
    $('html').ajaxStart(function() {
        $(this).addClass('busy');
    });
    $('html').ajaxStop(function() {
        $(this).removeClass('busy');
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                const token = $('meta[name="csrf-token"]')
                    .attr('content');
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        }
    });
}

ajaxSetup();