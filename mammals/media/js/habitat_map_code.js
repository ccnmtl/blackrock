var markers = []
var the_map;
var breakdown_object;

function general_map_marker (name, where, map) {
    result = new google.maps.Marker ({
	'position' : new google.maps.LatLng( where[0], where [1])
	, 'map' : map
	, 'title': name // TODO add more interesting info.
    });
    return result
}



//habitat_disk_style


function habitat_disk_circle (habitat_id, where, style, map) {
  c = new google.maps.Circle({
      center:  new google.maps.LatLng( where[0], where [1]),
      map: map,

   });
  c.setOptions (style);
  return  c;
}


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
    //console.log (result);
    return result;
}



function addSimpleMap(mapInstance) {
    the_map = mapInstance;
    var habitat_colors_obj = JSON.parse(jQuery ('#habitat_colors_div')[0].innerHTML);
    
    
    
    function habitat_marker (habitat_id, name, where, map) {




        //console.log (habitat_id);
        //console.log (habitat_colors_obj[habitat_id]);
        the_rgb = habitat_colors_obj[habitat_id];
        
        
        
        //console.log (habitat_disk_circle(
        style = habitat_disk_style;
        style['fillColor'] = to_google_color (the_rgb);
        style['name']      = name;
        
        
        // style['fillColor'] =  habitat_colors_obj[habitat_id];
          c = new google.maps.Circle({
              center:  new google.maps.LatLng( where[0], where [1]),
              map: map,

           });
          c.setOptions (style);
          //return  c;
        /*
        result = new google.maps.Marker ({
	        'position' : new google.maps.LatLng( where[0], where [1])
	        , 'map' : map
	        , 'title': name // TODO add more interesting info.
            });
        */
        


        function show_info_window (event) {
            //alert ('hi');
            the_infowindow = new google.maps.InfoWindow();
            the_infowindow.setContent( name );
            the_infowindow.setPosition(event.latLng);
            the_infowindow.open(the_map);
        }



        google.maps.event.addListener(c, 'click', show_info_window);
        
        return c;
    }
    
    map_data = JSON.parse(jQuery('#map_data')[0].innerHTML);
    for (var i = 0; i < map_data.length; i++) {
        if (map_data[i]['where'][0] != 0) {
            // console.log (map_data[i]['habitat_id']);
            habitat_id = map_data[i]['habitat_id'];
	        // markers.push ( general_map_marker (map_data[i]['name'], map_data[i]['where'], mapInstance ));	        
	        new_marker = habitat_marker (habitat_id,   map_data[i]['name'], map_data[i]['where'], mapInstance );
            markers.push ( new_marker);
        }
    }
    show_little_habitat_disks();
    show_breakdown_numbers();
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



function show_breakdown_for_facet (the_facet, the_checkboxes) {
    for (var i = 0; i < the_checkboxes.length; i++) {
        var the_checkbox = the_checkboxes[i];
        var how_many = breakdown_object[the_facet] [the_checkbox.value]
        if ( how_many ) {
            say_how_many (the_checkbox, how_many);
        }
    }
}


function draw_disk_html (disk_path) {
    return "<img src=" + disk_path + "/>" ;

}





function show_little_habitat_disks() {
    var little_habitat_disks_obj = JSON.parse(jQuery ('#little_habitat_disks_div')[0].innerHTML);
    function show_a_disk (i, checkbox) {
        var habitat_id = checkbox.value;
        var disk_path = little_habitat_disks_obj[habitat_id];
        if (disk_path != '') {
            jQuery(checkbox.parentElement).prepend ( draw_disk_html(disk_path) );    
        }else {
            console.log ( habitat_id);
        }
    }
    jQuery.each (jQuery ('input[name="trap_habitat" ]'), show_a_disk);
}

function show_breakdown_numbers () {
    // Suggest ways to break down the search.
    // If you narrow the search by checking more boxes,how many spots would remain on the map ?
    breakdown_object = JSON.parse(jQuery ('#breakdown')[0].innerHTML);
    if (isEmpty (breakdown_object)) {
        return;
    }
    
    var facets = {
         'habitat' :       jQuery ('input[name="trap_habitat" ]')
        ,'species' :       jQuery ('input[name="trap_species" ]')
        ,'school'  :       jQuery ('input[name="trap_school"  ]')
        ,'trap_success'  : jQuery ('input[name="trap_success" ]')
    }    
    jQuery.each ( facets, show_breakdown_for_facet);
        
}



function say_how_many (the_checkbox, how_many) {
    jQuery(the_checkbox.parentElement).append ( ' (' + how_many + ')' );
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
