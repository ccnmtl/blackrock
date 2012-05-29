var grid_json;


function addGrid(mapInstance) {
    if (is_sandbox()) {
         jQuery('#grid_form')[0].action =   '/mammals/sandbox/grid_square/';
    } else {
        jQuery('#grid_form')[0].action =   '/mammals/grid_square/';
    }

    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), mapInstance);
        grid_json [i]['grid_rectangle'] = rect;
        attach_info (grid_json[i]);
        map_bounds.extend(lat_lng_from_point(box[4] ));
        add_square_difficulty (i, grid_json [i]['access_difficulty']);
        
        jQuery ('#difficulty_menu_select').change (function (eee) {
            show_squares (eee.currentTarget.value);
        });
    }
    
    
    // this works but it's really annoying.
    /*
    viewer_location = user_location(mapInstance);
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    */
    
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
}





function box_info_from_grid_obj(obj) {
    //TODO: remove this adapter.
    return {
        'box':                 obj['corner_obj'],
        'row' :                obj['row'],
        'column' :             obj['column'],
        'label':               obj['label'],
        'access_difficulty':   obj['access_difficulty'],
    }
}



difficulty_map = {}

function add_square_difficulty(square_index, difficulty) {
    //console.log ('adding_difficulty' + " square ix" + square_index + " diff: " + difficulty);
    if (difficulty_map.hasOwnProperty (difficulty)) {
        difficulty_map[difficulty].push (square_index);
    }
    else {
        difficulty_map[difficulty] = [ square_index ];
    }
    //console.log (JSON.stringify(difficulty_map));

}

function eligible_squares (maximum_difficulty) {
    result = [];
    for (difficulty in difficulty_map) {
        //console.log ("adding difficulty " + difficulty );
        if (difficulty <= maximum_difficulty) {
            //console.log ('adding');
            result = result.concat (difficulty_map[difficulty])
        }
        //console.log ("eligible squares is now " +  JSON.stringify(result));
    }
    return result;
}


function random_index (an_array) {
    return Math.floor(Math.random() * an_array.length)
}

function random_item (an_array) {
    return an_array [random_index(an_array)];
}

function axe_square (sq) {
    sq['grid_rectangle'].setOptions (square_styles['hidden']['unselected']  );
    google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseover');
    google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseout');
}


function show_squares (difficulty_level) {
    // show all the squares up to and including a particular level of difficulty of access.
    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq ['access_difficulty'] > difficulty_level) {
            //console.log ('hiding square ' + i);
            axe_square (sq);
        } else {
            sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']  );
            attach_info (sq);
        }
    }
}


function pick_a_square (difficulty_level) {
    max_difficulty = 5;
    if (difficulty_level == -1) {
        //alert ('showing all');
        difficulty_level = max_difficulty;
    }
    else {
        square_ids_to_choose_from = eligible_squares (difficulty_level);
        the_id = random_item(square_ids_to_choose_from);
        return grid_json[the_id];
    }

    return random_item(grid_json);
}



function suggest_square() {
    // TODO: select only from squares of a particular length:
    suggested_square = pick_a_square (-1);
    info = box_info_from_grid_obj(suggested_square);
    
    decorate_suggested_square (suggested_square);
    //decorate_suggested_square (suggested_square.grid_rectangle);
    display_info_about_square (info)
}

function unsuggest_square() {
    if (typeof(undecorate_suggested_square) == "function") {
        undecorate_suggested_square();
    }
}

square_styles = {
    'hidden' : {
        'selected' : {
            fillOpacity     : 0.0
            ,strokeOpacity     : 0.0
        }
        ,'unselected' : {
            fillOpacity     : 0.0
            ,strokeOpacity     : 0.0
        }
    }
    ,'suggested_square' : {
        'selected' : {
            fillOpacity     : 1.0
            ,fillColor      : 'red'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
        ,'unselected' : {
            fillOpacity     : 0.6
            ,fillColor      : 'red'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
    }
    ,'regular': {
        'selected' : {
            fillOpacity     : 0.3
            ,fillColor      : 'blue'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
        ,'unselected' : {
            fillOpacity     : 0.1
            ,fillColor      : 'blue'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
    }
}




function attach_info(sq) {
    rect = sq['grid_rectangle']
    add_regular_mouseover (rect);
    add_regular_mouseout (rect);
    google.maps.event.addListener(rect, 'mouseover', function() {
        display_info_about_square (box_info_from_grid_obj (sq));
    });
    google.maps.event.clearListeners(rect, 'click');
    google.maps.event.addListener(rect, 'click', function() {
        jQuery('#grid_form')[0].submit();
    });
}

function decorate_suggested_square (sq) {
    rect = sq['grid_rectangle'];
    unsuggest_square();
    rect.setOptions (square_styles['suggested_square']['unselected']);
    add_special_mouseout  (rect);
    add_special_mouseover (rect);
    undecorate_suggested_square = function () {
        attach_info(sq);
        sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']);
    }
}


function display_info_about_square (info) {

    
    //console.log ('Square # ' + info['label']);
    
    /// These two lines set the value of the square in the hidden form values.
    jQuery('#selected_block_center_y') [0].value = info['box'][4][0];
    jQuery('#selected_block_center_x') [0].value = info['box'][4][1];

    // show values in the box:
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
    jQuery('#block_info')       [0].innerHTML =  'Square # ' + info['label']+ ':'
    jQuery('#block_difficulty') [0].innerHTML =  'Access difficulty: Level ' + info['access_difficulty']+ '.'
    jQuery('.grid_border_coords_table').show();
}


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
