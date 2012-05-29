var grid_json;

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

function show_squares (difficulty_level) {
    // show all the squares up to and including a particular level of difficulty of access.
    for (var i = 0; i < grid_json.length; i++) {
        sq = grid_json [i];
        if (sq ['access_difficulty'] > difficulty_level) {
            //console.log ('hiding square ' + i);
            sq['grid_rectangle'].setOptions (square_styles['hidden']['unselected']  );
            google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseover');
            google.maps.event.clearListeners(sq['grid_rectangle'], 'mouseout');
        } else {
            sq['grid_rectangle'].setOptions (square_styles['regular']['unselected']  );
            attach_info (sq['grid_rectangle'], box_info_from_grid_obj (sq));
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

function addGrid(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    //alert (JSON.stringify(grid_json[0]));
    //return;
    
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), mapInstance);
        attach_info (rect, box_info_from_grid_obj (grid_json[i]));
        map_bounds.extend(lat_lng_from_point(box[4] ));
        grid_json [i]['grid_rectangle'] = rect
        
        //console.log (i);
        //console.log (grid_json [i]['access_difficulty']);
        
        add_square_difficulty (i, grid_json [i]['access_difficulty']);
            
            jQuery ('#difficulty_menu_select').change (function (eee) {
                show_squares (eee.currentTarget.value);
                //show_squares( 1);
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



function suggest_square() {
    // TODO: select only from squares of a particular length:
    suggested_square = pick_a_square (-1);
    decorate_suggested_square (suggested_square.grid_rectangle);
    info = box_info_from_grid_obj(suggested_square);
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





function attach_info(rect, info) {
   /*
   google.maps.clearListeners(rect, 'mouseover');
   google.maps.clearListeners(rect, 'mouseout');
   */
    
    add_regular_mouseover (rect);
    add_regular_mouseout (rect);
    google.maps.event.addListener(rect, 'mouseover', function() {
        display_info_about_square (info);
    });
    google.maps.event.addListener(rect, 'click', function() {
     the_form = jQuery('#grid_form')[0]
     if (is_sandbox()) {
         the_form.action =   '/mammals/sandbox/grid_square/';
    } else {
        the_form.action =   '/mammals/grid_square/';
    }
     the_form.submit();
  });
}

function decorate_suggested_square (suggested_square) {
    
    unsuggest_square();
    suggested_square.setOptions (square_styles['suggested_square']['unselected']);
    add_special_mouseout  (suggested_square);
    add_special_mouseover (suggested_square);
    
    undecorate_suggested_square = function () {
        suggested_square.setOptions (square_styles['regular']['unselected']);
        add_regular_mouseover(suggested_square);
        add_regular_mouseout(suggested_square);
    }
}

function display_info_about_square (info) {
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
    jQuery('#selected_block_center_y') [0].value = info['box'][4][0];
    jQuery('#selected_block_center_x') [0].value = info['box'][4][1];
    jQuery('#block_info')       [0].innerHTML =  'Square # ' + info['label']+ ':'
    jQuery('#block_difficulty') [0].innerHTML =  'Access difficulty: Level ' + info['access_difficulty']+ '.'
    jQuery('.grid_border_coords_table').show();
}


function add_regular_mouseover (rect) {
    //google.maps.clearListeners(rect, 'mouseover'); /// hmm... this would turn off the display_info_about_square.
    google.maps.event.addListener(rect, 'mouseover', function() {
    rect.setOptions (square_styles['regular']['selected']);
  });
}

function add_regular_mouseout (rect) {
  //google.maps.clearListeners(rect, 'mouseout');
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions (square_styles['regular']['unselected']);
  });
}

function add_special_mouseover (rect) {
   //google.maps.clearListeners(rect, 'mouseover');
    google.maps.event.addListener(rect, 'mouseover', function() {
    rect.setOptions (square_styles['suggested_square']['selected']);
    });
}

function add_special_mouseout (rect) {
   //google.maps.clearListeners(rect, 'mouseout');
    google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions (square_styles['suggested_square']['unselected']);
    });
}
