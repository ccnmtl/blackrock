var markers = []
var the_map;
//var breakdown_object;

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



function addHabitatMap(mapInstance) {
    // this is called from on high.
    the_map = mapInstance;
    breakdown_object = JSON.parse(jQuery ('#breakdown')[0].innerHTML);
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    refresh_map(mapInstance, breakdown_object, map_data);
    decorate_page();
}

function ajax_search() {
    jQuery.ajax({
        data: jQuery('#the_habitat_search_form').serialize(),
        type: 'POST',
        url: '/mammals/ajax_search/',
        success: function(response) {
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
            the_infowindow = new google.maps.InfoWindow();
            the_infowindow.setContent( name );
            the_infowindow.setPosition(event.latLng);
            the_infowindow.open(the_map);
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
    show_breakdown_numbers( breakdown_object);
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
    
    jQuery ('.breakdown_number_span').remove();

    console.log (breakdown_object);
    
    // Suggest ways to break down the search.
    // If you narrow the search by checking more boxes,how many spots would remain on the map ?
    
    if (isEmpty (breakdown_object)) {
        return;
    }
    var facets = {
         'habitat' :       jQuery ('input[name="trap_habitat" ]')
        ,'species' :       jQuery ('input[name="trap_species" ]')
        ,'school'  :       jQuery ('input[name="trap_school"  ]')
        ,'trap_success'  : jQuery ('input[name="trap_success" ]')
    }
    
    
    res = [];
    jQuery.each (facets, function (k, v) { res.push ( {'k': k, 'v': v } ); }  );
    
    
    //jQuery.each ( facets, show_breakdown_for_facet);    
    
    
    //function show_breakdown_for_facet (the_facet, the_checkboxes) {
    
    
    for (var j = 0; j < res.length; j++) {
    
        the_facet      = res[j]['k'];
        the_checkboxes = res[j]['v'];
        //console.log (the_facet);
        
        for (var i = 0; i < the_checkboxes.length; i++) {
            var the_checkbox = the_checkboxes[i];
            var how_many = breakdown_object[the_facet] [the_checkbox.value]
            if ( how_many ) {
                say_how_many (the_checkbox, how_many);
            }
        }
    }


    
    
}


function say_how_many (the_checkbox, how_many) {
    jQuery(the_checkbox.parentElement).append ( '<span class = "breakdown_number_span"> (' + how_many + ') </span>' );
    
    
    //console.log (the_checkbox.value);
    //console.log (' --> ' + how_many);
}








///////////// HABITAT LEGEND DISKS:



function draw_disk_html (disk_path) {
    return "<img class='habitat_legend_disk' src='" + disk_path + "'/>" ;
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
    jQuery.each (jQuery ('input[name="trap_habitat" ]'), show_a_disk);
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
    /*
    var trails_kmllayer = new Portal.Layer("trails", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/trails.kml", true);
    self.layers["trails"] = trails_kmllayer;
    trails_kmllayer.instance.setMap(self.mapInstance);
    
    var roads_kmllayer = new Portal.Layer("roads", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/roads.kml", true);
    self.layers["roads"] = roads_kmllayer;
    roads_kmllayer.instance.setMap(self.mapInstance);
    */
    var buildings_kmllayer = new Portal.Layer("roads", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/buildings.kml", true);
    self.layers["buildings"] = buildings_kmllayer;
    buildings_kmllayer.instance.setMap(self.mapInstance);
    
}

