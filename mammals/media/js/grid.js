var grid_json;
var terrain_difficulty_map = {}
var access_difficulty_map = {}


function addGrid(mapInstance) {

    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), mapInstance);
        grid_json [i]['grid_rectangle'] = rect;
        attach_info (grid_json[i]);
        map_bounds.extend(lat_lng_from_point(box[4] ));
        add_square_difficulty (i, grid_json [i]['access_difficulty'],   grid_json [i]['terrain_difficulty']);
        
    }
    jQuery ('#access_difficulty_menu_select').change (show_squares);
    jQuery ('#difficulty_menu_select').change (show_squares);
    
    // if you just came from the square page, paint the square you just visited:
    deal_with_just_visited_block();
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    }
    // this works but it's really annoying.
    /*
    viewer_location = user_location(mapInstance);
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    */ 
}


function add_square_difficulty(square_index, access_difficulty, terrain_difficulty) {
    console.log('adding square difficulty');
    if (terrain_difficulty_map.hasOwnProperty (terrain_difficulty)) {
        terrain_difficulty_map[terrain_difficulty].push (square_index);
    }
    else {
        terrain_difficulty_map[terrain_difficulty] = [ square_index ];
    }
    
    if (access_difficulty_map.hasOwnProperty (access_difficulty)) {
        access_difficulty_map[access_difficulty].push (square_index);
    }
    else {
        access_difficulty_map[access_difficulty] = [ square_index ];
    }
    
}

function eligible_squares () {
    var access_difficulty_level = parseInt(jQuery('#access_difficulty_menu_select').val());
    var terrain_difficulty_level = parseInt(jQuery('#difficulty_menu_select').val());
    result = [];
    
        
    //var terrain_difficulty_map = {}
    //var access_difficulty_map = {}

    /*
    for (difficulty in terrain_difficulty_map) {
        if (difficulty <= terrain_difficulty_level) {
            result = result.concat (terrain_difficulty_map[difficulty])
        }
    }
    */
    
    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq ['access_difficulty'] > access_difficulty_level || sq ['terrain_difficulty'] > terrain_difficulty_level) {
            //axe_square (sq);
            // square is too hard. don't choose it.
        } else {
            //sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']  );
            //attach_info (sq);
            result = result.concat (i);
        }
    }
    
    console.log (JSON.stringify(result));
    
    return result;
}

/*


function all_squares () {
    maximum_difficulty = 5;
    result = [];
    for (difficulty in terrain_difficulty_map) {
        if (difficulty <= maximum_difficulty) {
            result = result.concat (terrain_difficulty_map[difficulty])
        }
    }
    return result;
}


function new_all_squares () {
    result = [];
    for (difficulty in terrain_difficulty_map) {
            result = result.concat (terrain_difficulty_map[difficulty])
    }
    return result;
}
*/



function axe_square (sq) {
    sq['grid_rectangle'].setOptions (square_styles['hidden']['unselected']  );
    google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseover');
    google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseout');
}


function show_squares () {
    var access_difficulty_level = parseInt(jQuery('#access_difficulty_menu_select').val());
    var terrain_difficulty_level = parseInt(jQuery('#difficulty_menu_select').val());
    // show all the squares up to and including a particular level of difficulty of access.
    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq ['access_difficulty'] > access_difficulty_level || sq ['terrain_difficulty'] > terrain_difficulty_level) {
            axe_square (sq);
        } else {
            sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']  );
            attach_info (sq);
        }
    }
}



function random_index (an_array) {
    return Math.floor(Math.random() * an_array.length)
}

function random_item (an_array) {
    return an_array [random_index(an_array)];
}



function suggest_square() {
    //console.log ("HEY");
    
    suggested_square =  grid_json[random_item(eligible_squares ())];
    
    //suggested_square = random_item(grid_json);
    console.log (suggested_square);
    decorate_suggested_square (suggested_square);
    //decorate_suggested_square (suggested_square.grid_rectangle);
    display_info_about_square (suggested_square);
}


function decorate_suggested_square (sq) {
    unsuggest_square();
    jQuery ('.randomize_again_hint').show();
    sq['grid_rectangle'].setOptions (square_styles['suggested_square']['unselected']);
    add_special_mouseout  (sq['grid_rectangle']);
    add_special_mouseover (sq['grid_rectangle']);
    undecorate_suggested_square = function () {
        sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']);
        attach_info(sq);
    }
}


function unsuggest_square() {
    jQuery ('.randomize_again_hint').hide();
    if (typeof(undecorate_suggested_square) == "function") {
        undecorate_suggested_square();
    }
}


function deal_with_just_visited_block () {
    if (jQuery('#selected_block').length == 0) { // don't bother doing this  on sandbox
        return;
    }
    selected_block_id = jQuery ('#selected_block')[0].innerHTML;
    if ( selected_block_id == '') {
        return;
    }


    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq['database_id'] == selected_block_id) {
           sq['grid_rectangle'].setOptions (square_styles['just_visited']['unselected']);
           add_just_visited_mouseout  (sq['grid_rectangle']);
           add_just_visited_mouseover (sq['grid_rectangle'], sq);
        }
    }
}

function make_square_clickable (rect) {
    // when the user clicks a square, take them to the grid square page, submitting the form
    // to the appropriate url.
    google.maps.event.clearListeners(rect, 'click');
    google.maps.event.addListener(rect, 'click', function() {
        if (is_sandbox()) {
             jQuery('#grid_form')[0].action =   '/mammals/sandbox/grid_square/';
        } else {
            jQuery('#grid_form')[0].action =   '/mammals/grid_square/';
        }
        jQuery('#grid_form')[0].submit();
    });
}

function attach_info(sq) {
    rect = sq['grid_rectangle']
    add_regular_mouseover (rect);
    add_regular_mouseout (rect);
    google.maps.event.addListener(rect, 'mouseover', function() {
        display_info_about_square (sq);
    });
    make_square_clickable (rect);
}



function display_info_about_square (info) {
    
    /// These two lines set the value of the square in the hidden form values.
    jQuery('#selected_block_center_y') [0].value = info['corner_obj'][4][0];
    jQuery('#selected_block_center_x') [0].value = info['corner_obj'][4][1];
    
    if (!is_sandbox()) {
        //console.log (info['database_id']);
        //jQuery('#selected_block_database_id') [0].value = info['database_id'];
        //jQuery('#selected_block_database_id') [0].value = info['database_id'];
    	jQuery('#selected_block_database_id') [0].value = info['database_id'];
    }

    // show values in the box:
    jQuery('#bl')[0].innerHTML = trimpoint(info['corner_obj'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['corner_obj'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['corner_obj'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['corner_obj'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['corner_obj'][4]);
        
    if (is_sandbox()) {
        jQuery('#block_info')[0].innerHTML =  'Row ' + info['row'] + ", column " + info['column'];
    }
    else {
        jQuery('#block_info')       [0].innerHTML =  'Square no.: ' + info['battleship_coords'];
    }
    jQuery('#block_difficulty') [0].innerHTML =  '<br/> <b>Access difficulty level:</b> '+ info['access_difficulty'] 
    + ' <br/> <b>Terrain difficulty level:</b> ' + info['terrain_difficulty'] ;
    
    
    
    ;
    jQuery('.grid_border_coords_table').show();
}



//TODO: DRY up the below functions.
function add_regular_mouseover (rect) {
    google.maps.event.clearListeners(rect, 'mouseover');
    google.maps.event.addListener(rect, 'mouseover', function() {
    rect.setOptions (square_styles['regular']['selected']);
  });
}

function add_regular_mouseout (rect) {
    google.maps.event.clearListeners(rect, 'mouseout');
    google.maps.event.addListener(rect, 'mouseout', function() {
        rect.setOptions (square_styles['regular']['unselected']);
    });
}

function add_special_mouseover (rect) {
    google.maps.event.clearListeners(rect, 'mouseover');
    google.maps.event.addListener(rect, 'mouseover', function() {
        rect.setOptions (square_styles['suggested_square']['selected']);
    });
}

function add_special_mouseout (rect) {
    google.maps.event.clearListeners(rect, 'mouseout');
    google.maps.event.addListener(rect, 'mouseout', function() {
        rect.setOptions (square_styles['suggested_square']['unselected']);
    });
}

function add_just_visited_mouseover (rect, sq) {
    google.maps.event.clearListeners(rect, 'mouseover');
    google.maps.event.addListener(rect, 'mouseover', function() {
        display_info_about_square (sq);
        rect.setOptions (square_styles['just_visited']['selected']);
    });
}

function add_just_visited_mouseout (rect) {
    google.maps.event.clearListeners(rect, 'mouseout');
    google.maps.event.addListener(rect, 'mouseout', function() {
        rect.setOptions (square_styles['just_visited']['unselected']);
    });
}

